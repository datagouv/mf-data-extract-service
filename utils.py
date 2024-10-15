import concurrent.futures
import json
import logging
import os
import random
import requests
from requests.exceptions import RequestException, Timeout
import shutil
import time
from datetime import datetime, timedelta
from typing import List, Optional, TypedDict
import re
import pygrib

from minio import Minio, datatypes
from minio.error import S3Error

from config import (
    APIKEY_DATAGOUV,
    BATCH_URL_SIZE_PACKAGE,
    DATAGOUV_URL,
    MAX_LAST_BATCHES,
    MINIO_BUCKET,
    MINIO_PASSWORD,
    MINIO_URL,
    MINIO_PUBLIC_URL,
    MINIO_USER,
    MINIO_SECURE,
    PACKAGES,
    ENV_NAME,
)


class File(TypedDict):
    source_path: str
    source_name: str
    dest_path: str
    dest_name: str
    content_type: Optional[str]


def get_minio_file(
    MINIO_URL: str,
    MINIO_BUCKET: str,
    MINIO_USER: str,
    MINIO_PASSWORD: str,
    minio_path: str,
    target_path: str,
):
    client = Minio(
        MINIO_URL,
        access_key=MINIO_USER,
        secret_key=MINIO_PASSWORD,
        secure=MINIO_SECURE,
    )

    found = client.bucket_exists(MINIO_BUCKET)
    if found:
        client.fget_object(MINIO_BUCKET, minio_path, target_path)


def send_files(
    MINIO_URL: str,
    MINIO_BUCKET: str,
    MINIO_USER: str,
    MINIO_PASSWORD: str,
    list_files: List[File]
):
    client = Minio(
        MINIO_URL,
        access_key=MINIO_USER,
        secret_key=MINIO_PASSWORD,
        secure=MINIO_SECURE,
    )

    found = client.bucket_exists(MINIO_BUCKET)

    if found:
        for file in list_files:
            is_file = os.path.isfile(
                os.path.join(file["source_path"], file["source_name"])
            )
            if is_file:
                dest_path = f"{file['dest_path']}{file['dest_name']}"
                client.fput_object(
                    MINIO_BUCKET,
                    dest_path,
                    os.path.join(file["source_path"], file["source_name"]),
                    content_type=(
                        file['content_type']
                        if 'content_type' in file
                        else None
                    )
                )
            else:
                raise Exception(
                    f"file {file['source_path']}{file['source_name']} "
                    "does not exists"
                )
    else:
        raise Exception(f"Bucket {MINIO_BUCKET} does not exists")


def get_files_from_prefix(
    MINIO_URL: str,
    MINIO_BUCKET: str,
    MINIO_USER: str,
    MINIO_PASSWORD: str,
    prefix: str,
):
    client = Minio(
        MINIO_URL,
        access_key=MINIO_USER,
        secret_key=MINIO_PASSWORD,
        secure=MINIO_SECURE,
    )
    found = client.bucket_exists(MINIO_BUCKET)
    if found:
        list_objects = []
        objects = client.list_objects(
            MINIO_BUCKET,
            prefix=f"{prefix}",
            recursive=True
        )
        for obj in objects:
            list_objects.append(obj.object_name)
        return list_objects
    else:
        raise Exception(f"Bucket {MINIO_BUCKET} does not exists")


def delete_files_prefix(
    MINIO_URL: str,
    MINIO_BUCKET: str,
    MINIO_USER: str,
    MINIO_PASSWORD: str,
    prefix: str,
):
    """/!\ USE WITH CAUTION"""
    client = Minio(
        MINIO_URL,
        access_key=MINIO_USER,
        secret_key=MINIO_PASSWORD,
        secure=MINIO_SECURE,
    )

    try:
        # List objects in the specified folder
        objects = client.list_objects(
            MINIO_BUCKET,
            prefix=prefix,
            recursive=True
        )

        # Create a list of object names to delete
        objects_to_delete = [obj.object_name for obj in objects]

        # Delete all objects in the folder
        for obj_name in objects_to_delete:
            client.remove_object(MINIO_BUCKET, obj_name)

        logging.info(
            f"All objects with prefix '{prefix}' deleted successfully."
        )

    except S3Error as e:
        logging.info(f"Error: {e}")


def get_last_batch_hour():
    now = datetime.now()
    if now.hour < 6:
        batch_hour = 0
    elif now.hour < 12:
        batch_hour = 6
    elif now.hour < 18:
        batch_hour = 12
    elif now.hour >= 18:
        batch_hour = 18
    batch_time = now.replace(
        second=0,
        microsecond=0,
        minute=0,
        hour=batch_hour
    )
    return batch_time


def download_url(url, meta_urls, retry, current_folder):
    if retry != 0:
        if retry != 5:
            print("Retry " + str(5-retry) + "for " + url)
        try:
            filename = meta_urls[url + ":filename"]
            headers = meta_urls[url + ":headers"]
            with requests.get(
                url,
                stream=True,
                headers=headers,
                timeout=60
            ) as r:
                r.raise_for_status()
                with open(current_folder + "/" + filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=32768):
                        f.write(chunk)
        except Timeout:
            logging.info("The request timed out. for " + url)
        except Exception:
            download_url(url, meta_urls, current_folder, retry-1)
    else:
        logging.info(
            f"EXCEPTION: {meta_urls[url+':filename']} "
            "cannot be downloaded after 5 tries"
        )


def send_to_minio(url, meta_urls, current_folder):
    send_files(
        MINIO_URL=MINIO_URL,
        MINIO_BUCKET=MINIO_BUCKET,
        MINIO_USER=MINIO_USER,
        MINIO_PASSWORD=MINIO_PASSWORD,
        list_files=[
            {
                "source_path": current_folder + "/",
                "source_name": meta_urls[url + ":filename"],
                "dest_path": (
                    meta_urls[url + ":minio_path"]
                ),
                "dest_name": meta_urls[url + ":filename"],
            }
        ],
    )
    logging.info(f"{meta_urls[url+':filename']} sent to minio")


def test_file_structure(filepath):
    # open and check that grib file is properly structured
    grib = pygrib.open(filepath)
    for msg in grib:
        try:
            msg.values.shape
        except:
            return False
    return True


def process_url(url, meta_urls, current_folder):
    download_url(url, meta_urls, 5, current_folder)
    if test_file_structure(current_folder + "/" + meta_urls[url + ":filename"]):
        send_to_minio(url, meta_urls, current_folder)
    else:
        print(meta_urls[url + ":filename"], "is badly structured, deleting...")
        os.remove(current_folder + "/" + meta_urls[url + ":filename"])


def remove_and_create_folder(folder_path, toCreate):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    if toCreate:
        os.makedirs(folder_path)


def check_if_data_available(batches, url, apikey):
    try:
        r = requests.get(url, headers={"apikey": apikey}, timeout=10)
        new_batches = []
        try:
            if "links" in r.json():
                for batch in batches:
                    for link in r.json()["links"]:
                        if batch in link["href"]:
                            new_batches.append(batch)
            return new_batches
        except Exception:
            logging.info("--- ERROR WITH MF API ----")
    except RequestException as e:
        logging.info(f"Erreur de connexion : {e}")


def send_processing_file(value):
    data = {"processing": value}
    with open("./processing.json", "w") as fp:
        json.dump(data, fp)
    send_files(
        MINIO_URL=MINIO_URL,
        MINIO_BUCKET=MINIO_BUCKET,
        MINIO_USER=MINIO_USER,
        MINIO_PASSWORD=MINIO_PASSWORD,
        list_files=[
            {
                "source_path":  "./",
                "source_name": "processing.json",
                "dest_path": "",
                "dest_name": "processing.json"
            }
        ],
    )
    os.remove("./processing.json")


# def check_if_ongoing_process():
#     processing = False
#     try:
#         get_minio_file(
#             MINIO_URL,
#             MINIO_BUCKET,
#             MINIO_USER,
#             MINIO_PASSWORD,
#             "processing.json",
#             "/tmp/processing.json"
#         )
#         with open("/tmp/processing.json", "r") as fp:
#             data = json.load(fp)
#         if data["processing"]: processing = data["processing"]
#     except:
#         logging.info("no file, creating")

#     if processing:
#         logging.info("Already processing - skip")
#         sys.exit()

#     send_processing_file(True)


def get_latest_theorical_batches(ctx):
    batches = []
    if ctx != "arome":
        for i in range(MAX_LAST_BATCHES):
            batches.append((
                get_last_batch_hour() - timedelta(hours=6*i)
            ).strftime("%Y-%m-%dT%H:%M:%SZ"))
    else:
        for i in range(MAX_LAST_BATCHES*2):
            batches.append((
                get_last_batch_hour() - timedelta(hours=3*i)
            ).strftime("%Y-%m-%dT%H:%M:%SZ"))
        batch3hlater = datetime.strptime(
            batches[0], "%Y-%m-%dT%H:%M:%SZ"
        ) + timedelta(hours=3)
        if batch3hlater < datetime.now():
            batches.append(batch3hlater.strftime("%Y-%m-%dT%H:%M:%SZ"))

    logging.info(batches)
    tested_batches = {}
    for PACK in PACKAGES:
        if PACK["type_package"] in ctx.split(","):
            if PACK["detail_package"]:
                test_batch = PACK["type_package"] + "-" + PACK["detail_package"]
            else:
                test_batch = PACK["type_package"]
            if test_batch not in tested_batches:
                tested_batches[test_batch] = check_if_data_available(
                    batches,
                    PACK["check_availability_url"],
                    PACK["apikey"]
                )
    return batches, tested_batches


def construct_all_possible_files(batches, tested_batches):
    list_files = []
    meta_urls = {}
    minio_paths = []
    family_paths = {}
    for batch in batches:
        for family_package in PACKAGES:
            family_path = []

            if family_package["detail_package"]:
                test_batch = (
                    family_package["type_package"] + "-"
                    + family_package["detail_package"]
                )
            else:
                test_batch = family_package["type_package"]

            if (
                tested_batches
                and test_batch in tested_batches
                and batch in tested_batches[test_batch]
            ):
                for package in family_package["packages"]:
                    for timeslot in package["time"]:
                        headers = {
                            "Content-Type": "application/json; charset=utf-8",
                            "apikey": family_package["apikey"]
                        }
                        if family_package["detail_package"]:
                            base_path = (
                                family_package["type_package"] + "/"
                                + family_package["detail_package"]
                            )
                            base_name = (
                                family_package["type_package"] + "-"
                                + family_package["detail_package"]
                            )
                        else:
                            base_path = family_package["type_package"]
                            base_name = family_package["type_package"]

                        url = (
                            family_package["base_url"] + "/"
                            + family_package["grid"]
                            + "/packages/" + package["name"] + "/"
                            + family_package["product"]
                            + "?&referencetime=" + batch
                            + "&time=" + timeslot
                            + "&format=" + family_package["extension"]
                        )
                        filename = (
                            base_name + "__"
                            + family_package["grid"].replace("0.", "0")
                            + "__" + package["name"] + "__" + timeslot + "__"
                            + batch + "." + family_package["extension"]
                        )
                        minio_path = (
                            "pnt/" + batch + "/" + base_path + "/"
                            + family_package["grid"].replace("0.", "0") + "/"
                            + package["name"] + "/" + filename
                        )
                        list_files.append(filename)
                        meta_urls[url+":headers"] = headers
                        meta_urls[url+":filename"] = filename
                        meta_urls[url+":minio_path"] = minio_path.split(filename)[0]
                        meta_urls[filename+":url"] = url
                        meta_urls[minio_path+":url"] = url
                        meta_urls[minio_path+":base_name"] = base_name
                        minio_paths.append(minio_path)
                        family_path.append(minio_path)

            if family_package["type_package"] not in family_paths:
                family_paths[family_package["type_package"]] = []
            family_paths[family_package["type_package"]] = family_paths[
                family_package["type_package"]
            ] + family_path

    logging.info(str(len(list_files)) + " possible files")

    get_list_files = get_files_from_prefix(
        MINIO_URL=MINIO_URL,
        MINIO_BUCKET=MINIO_BUCKET,
        MINIO_USER=MINIO_USER,
        MINIO_PASSWORD=MINIO_PASSWORD,
        prefix="pnt/",
    )

    to_get = list(set(minio_paths) - set(get_list_files))

    logging.info(
        str(len(to_get))
        + " possible file(s) after removing already processed files"
    )

    if len(to_get) == 0:
        logging.info("no new data, exit")
        # send_processing_file(False)
        # sys.exit()
        return None

    family_urls = {}
    for fb in family_paths:
        family_urls[fb] = []
        for mpath in family_paths[fb]:
            if mpath in to_get:
                family_urls[fb].append(meta_urls[mpath+":url"])

    for fu in family_urls:
        random.shuffle(family_urls[fu])

    family_batches = {}
    for fu in family_urls:
        family_batches[fu] = [
            family_urls[fu][i:i+BATCH_URL_SIZE_PACKAGE[fu]]
            for i in range(0, len(family_urls[fu]), BATCH_URL_SIZE_PACKAGE[fu])
        ]

    return list_files, meta_urls, family_batches, get_list_files


def process_urls(
    family_batches,
    meta_urls,
    current_folder,
    max_workers,
    delay_between_batches,
    start
):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:

        max_iter = 0
        for fb in family_batches:
            if len(family_batches[fb]) > max_iter:
                max_iter = len(family_batches[fb])

        logging.info(str(max_iter) + " itérations")

        url_batches = []
        for i in range(max_iter):
            batch = []
            for fb in family_batches:
                if len(family_batches[fb]) > i:
                    batch = batch + family_batches[fb][i]
                    print(fb, len(family_batches[fb][i]))
            url_batches.append(batch)

        # url_batches = [
        #     urls[i:i+BATCH_URL_SIZE]
        #     for i in range(0, len(urls), BATCH_URL_SIZE)
        # ]
        batch_nb = 0
        for batch in url_batches:
            batch_nb += 1
            end = time.time()
            logging.info(
                f"Processing batch nb {batch_nb} -"
                f" time {str(round(end - start, 2))}s"
            )
            logging.info(str(len(batch)) + " urls to process in this batch")
            # Lancez les requêtes pour chaque URL dans le paquet simultanément
            futures = [
                executor.submit(process_url, url, meta_urls, current_folder)
                for url in batch
            ]

            # Pause d'une minute entre les paquets
            if batch_nb != max_iter:
                time.sleep(delay_between_batches)


def processing_each_possible_files(meta_urls, current_folder, family_batches):

    start = time.time()

    max_workers = 600
    delay_between_batches = 60  # Délai en secondes entre les paquets

    process_urls(
        family_batches,
        meta_urls,
        current_folder,
        max_workers,
        delay_between_batches,
        start
    )
    end = time.time()
    logging.info(f"Files processed in {str(round(end - start, 2))}s")


def reorder_resources(ctx):
    for package in PACKAGES:
        if package["type_package"] in ctx.split(","):
            res_list = []
            r = requests.get(
                f"{DATAGOUV_URL}/api/1/datasets/"
                + package["dataset_id_" + ENV_NAME]
            )
            data = r.json()
            for res in data["resources"]:
                res_list.append({
                    "title": res["title"],
                    "id": res["id"],
                    "did": package["dataset_id_" + ENV_NAME]
                })
            sorted_data = sorted(res_list, key=lambda x: x['title'])
            body = [{"id": x["id"]} for x in sorted_data]
            r = requests.put(
                f"{DATAGOUV_URL}/api/1/datasets/"
                f"{package['dataset_id_' + ENV_NAME]}/resources/",
                json=body,
                headers={"X-API-KEY": APIKEY_DATAGOUV}
            )
            if r.status_code == 200:
                logging.info(
                    "Reorder successful for dataset "
                    + package['dataset_id_' + ENV_NAME]
                )
            else:
                logging.info(f"Error on reordering, status code {r.status_code}")


def clean_old_runs_in_minio(batches):

    get_list_files_updated = get_files_from_prefix(
        MINIO_URL=MINIO_URL,
        MINIO_BUCKET=MINIO_BUCKET,
        MINIO_USER=MINIO_USER,
        MINIO_PASSWORD=MINIO_PASSWORD,
        prefix="pnt/",
    )

    old_dates = []
    keep_dates = []
    for file in get_list_files_updated:
        if (
            file.split(".")[0].split("__")[-1] < batches[-1]
            and file.split(".")[0].split("__")[-1] not in old_dates
        ):
            old_dates.append(file.split(".")[0].split("__")[-1])

        if (
            file.split(".")[0].split("__")[-1] >= batches[-1]
            and file.split(".")[0].split("__")[-1] not in keep_dates
        ):
            keep_dates.append(file.split(".")[0].split("__")[-1])

    if len(keep_dates) > 3:
        for od in old_dates:
            delete_files_prefix(
                MINIO_URL=MINIO_URL,
                MINIO_BUCKET=MINIO_BUCKET,
                MINIO_USER=MINIO_USER,
                MINIO_PASSWORD=MINIO_PASSWORD,
                prefix="pnt/"+od
            )


def get_package_from_name(name):
    prefix = name.split('__')[0]
    grille = name.split('__')[1]
    grille = grille[0] + '.' + ''.join(grille[1:])
    if '-' in prefix:
        # arome-om
        if prefix.count('-') == 2:
            return '-'.join(prefix.split('-')[:-1]), prefix.split('-')[-1], grille
        # vague-surcote
        if prefix.count('-') == 3:
            return '-'.join(prefix.split('-')[:-2]), '-'.join(prefix.split('-')[-2:]), grille
        raise Exception('Should not happen')
    return prefix, None, grille


def get_params(name, detail, grille):
    for p in PACKAGES:
        if p['type_package'] == name and p['grid'] == grille:
            if detail is None:
                return p
            elif p['detail_package'] == detail:
                return p
    raise Exception('Should not happen')


def publish_on_datagouv(current_folder, ctx):
    reorder = False
    get_list_files_updated = get_files_from_prefix(
        MINIO_URL=MINIO_URL,
        MINIO_BUCKET=MINIO_BUCKET,
        MINIO_USER=MINIO_USER,
        MINIO_PASSWORD=MINIO_PASSWORD,
        prefix="pnt/",
    )
    minio_files = {}
    # re-getting minio files as they have been updated
    for minio_path in get_list_files_updated:
        name = "__".join(
            minio_path.split("/")[-1].split(".")[0].split("__")[:-1]
        )
        date_file = minio_path.split("/")[-1].split(".")[0].split("__")[-1]
        if name not in minio_files or minio_files[name]['date'] < date_file:
            minio_files[name] = {'date': date_file, 'path': minio_path}

    # getting files currently on data.gouv
    datagouv_files = {}
    for package in PACKAGES:
        if package["type_package"] in ctx.split(","):
            r = requests.get(
                f"{DATAGOUV_URL}/api/1/datasets/"
                + package['dataset_id_' + ENV_NAME],
                headers={'X-fields': 'resources{id,url,type}'}
            )
            resources = r.json()["resources"]
            for resource in resources:
                if resource['type'] != 'main':
                    continue
                name = "__".join(
                    resource["url"].split("/")[-1].split(".")[0].split("__")[:-1]
                )
                date_file = resource["url"].split("/")[-1].split(".")[0].split("__")[-1]
                datagouv_files[name] = {
                    'date': date_file,
                    'path': resource["url"],
                    'extension': package["extension"],
                    'id': resource["id"],
                    'dataset_id': package['dataset_id_' + ENV_NAME],
                }

    for name in minio_files:
        if get_package_from_name(name)[0] not in ctx.split(","):
            continue
        # if the file is already on data.gouv and it's more recent on minio => upload
        if name in datagouv_files:
            if minio_files[name]['date'] > datagouv_files[name]['date']:
                reorder = True
                filename = (
                    name + "__"
                    + minio_files[name]['date']
                    + "." + datagouv_files[name]['extension']
                )
                body = {
                    "title": filename,
                    'url': (
                        f"https://{MINIO_PUBLIC_URL}/{MINIO_BUCKET}/"
                        + minio_files[name]["path"]
                    ),
                    'type': 'main',
                    'filetype': 'remote',
                    'format': datagouv_files[name]['extension'],
                }
                if os.path.exists(current_folder + '/' + filename):
                    body['filesize'] = os.path.getsize(
                        current_folder + '/' + filename
                    )
                r_put = requests.put(
                    f"{DATAGOUV_URL}/api/1/datasets/"
                    f"{datagouv_files[name]['dataset_id']}"
                    f"/resources/{datagouv_files[name]['id']}/",
                    json=body,
                    headers={"X-API-KEY": APIKEY_DATAGOUV}
                )
                if r_put.status_code == 200:
                    logging.info(
                        f"{name} updated in data.gouv.fr "
                        f"({datagouv_files[name]['date']} => "
                        f"{minio_files[name]['date']})"
                    )
        else:
            # if the file is not on data.gouv => upload (should not happend often)
            reorder = True
            package = get_params(*get_package_from_name(name))
            filename = (
                name + "__"
                + minio_files[name]['date']
                + "." + package['extension']
            )
            body = {
                "title": filename,
                'url': (
                    f"https://{MINIO_PUBLIC_URL}/{MINIO_BUCKET}/"
                    + minio_files[name]["path"]
                ),
                'type': 'main',
                'filetype': 'remote',
                'format': package['extension'],
            }
            if os.path.exists(current_folder + '/' + filename):
                body['filesize'] = os.path.getsize(
                    current_folder + '/' + filename
                )
            r_put = requests.post(
                f"{DATAGOUV_URL}/api/1/datasets/"
                f"{package['dataset_id_' + ENV_NAME]}"
                "/resources/",
                json=body,
                headers={"X-API-KEY": APIKEY_DATAGOUV}
            )
            if r_put.status_code == 200:
                logging.info(f"{name} created in data.gouv.fr")

    return reorder


def build_tree(paths):
    reg_datetime = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
    tree = {}
    oldest = "9999"
    for i, path in enumerate(paths):
        if isinstance(path, datatypes.Object):
            path = path.object_name
        parts = path.split('/')
        *dirs, file = parts
        dt = re.findall(reg_datetime, file)[0]
        oldest = min(dt, oldest)
        current_level = tree
        for idx, part in enumerate(dirs):
            if idx == len(dirs)-1:
                if not current_level.get(part):
                    current_level[part] = []
                current_level[part].append(file)
            elif part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
    return tree, oldest


def dump_and_send_tree():
    client = Minio(
        "object.files.data.gouv.fr",
    )
    files = client.list_objects(
        "meteofrance-pnt",
        prefix="pnt/",
        recursive=True
    )
    tree, oldest = build_tree(files)
    with open('./pnt_tree.json', 'w') as f:
        json.dump(tree, f)

    files = {"file": open("./pnt_tree.json", "rb",)}
    url = (
        f"{DATAGOUV_URL}/api/1/datasets/66d02b7174375550d7b10f3f/"
        "resources/ab77c9d0-3db4-4c2f-ae56-5a52ae824eeb/upload/"
    )
    r = requests.post(
        url,
        files=files,
        headers={"X-API-KEY": APIKEY_DATAGOUV},
    )
    r.raise_for_status()
    r = requests.put(
        url.replace("upload/", ""),
        json={"title": "Arborescence des dossiers sur le dépôt"},
        headers={"X-API-KEY": APIKEY_DATAGOUV},
    )
    r.raise_for_status()
    r = requests.put(
        f"{DATAGOUV_URL}/api/1/datasets/66d02b7174375550d7b10f3f/",
        json={
            "temporal_coverage": {
                "start": oldest + ".000000+00:00",
                "end": datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
        },
        headers={"X-API-KEY": APIKEY_DATAGOUV},
    )
    r.raise_for_status()
