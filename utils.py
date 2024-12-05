import concurrent.futures
import logging
import os
import random
import requests
from requests.exceptions import RequestException, Timeout
import shutil
import time
from datetime import datetime, timedelta
from typing import List, Optional, TypedDict, Iterator
import pygrib

from minio import Minio
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
    APPLICATION_ID,
)


class File(TypedDict):
    source_path: str
    source_name: str
    dest_path: str
    dest_name: str
    content_type: Optional[str]


client = Minio(
    MINIO_URL,
    access_key=MINIO_USER,
    secret_key=MINIO_PASSWORD,
    secure=MINIO_SECURE,
)
assert client.bucket_exists(MINIO_BUCKET)
LOG_PATH = "./logs/"


class Meteo_client(object):
    # code is courtesy of Météo France: https://portail-api.meteofrance.fr/web/fr/faq

    def __init__(self):
        self.session = requests.Session()

    def request(self, method, url, **kwargs):
        # First request will always need to obtain a token first
        if 'Authorization' not in self.session.headers:
            self.obtain_token()
        # Optimistically attempt to dispatch request
        response = self.session.request(method, url, **kwargs)
        if self.token_has_expired(response):
            # We got an 'Access token expired' response => refresh token
            self.obtain_token()
            # Re-dispatch the request that previously failed
            response = self.session.request(method, url, **kwargs)
        return response

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def token_has_expired(self, response):
        status = response.status_code
        content_type = response.headers['Content-Type']
        if status == 401 and 'application/json' in content_type:
            if 'Invalid JWT token' in response.json()['description']:
                return True
        return False

    def obtain_token(self):
        # Obtain new token
        access_token_response = requests.post(
            "https://portail-api.meteofrance.fr/token",
            data={'grant_type': 'client_credentials'},
            verify=False,
            allow_redirects=False,
            headers={'Authorization': 'Basic ' + APPLICATION_ID},
        )
        token = access_token_response.json()['access_token']
        # Update session with fresh token
        self.session.headers.update({'Authorization': f'Bearer {token}'})


meteo_client = Meteo_client()


def send_files(
    list_files: List[File]
) -> None:
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


def get_files_from_prefix(
    prefix: str,
    recursive: bool,
) -> Iterator:
    return client.list_objects(
        MINIO_BUCKET,
        prefix=prefix,
        recursive=recursive,
    )


def get_latest_files_from_package(
    package: str,
):
    runs = get_files_from_prefix(
        prefix="pnt/",
        recursive=False
    )
    # for better perfs, getting ony the latest 8 runs
    # (will be latest 4 for all except arome, which runs */3)
    for pref in sorted([f.object_name for f in runs])[-8:]:
        for f in get_files_from_prefix(
            prefix=pref + f"{package}/",
            recursive=True
        ):
            yield f.object_name


def delete_files_prefix(
    prefix: str,
) -> None:
    """/!\ USE WITH CAUTION"""
    try:
        for obj in get_files_from_prefix(prefix, recursive=True):
            client.remove_object(MINIO_BUCKET, obj.object_name)

        logging.info(
            f"All objects with prefix '{prefix}' deleted successfully."
        )

    except S3Error as e:
        logging.info(f"Error: {e}")


def get_last_batch_hour() -> datetime:
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


def download_url(url, meta_urls, retry, current_folder) -> None:
    if retry != 0:
        if retry != 5:
            logging.warning("Retry " + str(5-retry) + "for " + url)
        try:
            filename = meta_urls[url + ":filename"]
            with meteo_client.get(
                url,
                stream=True,
                timeout=60,
                # do we actually need these headers? response content type is binary
                headers={"Content-Type": "application/json; charset=utf-8"},
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


def send_to_minio(
    url: str,
    meta_urls: dict,
    current_folder: str,
) -> None:
    send_files(
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


def test_file_structure(filepath: str) -> bool:
    # open and check that grib file is properly structured
    try:
        grib = pygrib.open(filepath)
        for msg in grib:
            msg.values.shape
        return True
    except Exception as e:
        logging.warning(f"An error occured for {filepath}: `{e}`")
        return False


def log_and_send_error(filename):
    log_name = f"{filename.split('.')[0]}-{int(datetime.now().timestamp())}.log"
    with open(LOG_PATH + log_name, "w") as f:
        f.write(f"{filename};{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    send_files(
        list_files=[
            {
                "source_path": LOG_PATH,
                "source_name": log_name,
                "dest_path": "logs/",
                "dest_name": log_name,
            }
        ],
    )
    os.remove(LOG_PATH + log_name)


def process_url(
    url: str,
    meta_urls: dict,
    current_folder: str,
) -> None:
    download_url(url, meta_urls, 5, current_folder)
    if test_file_structure(current_folder + "/" + meta_urls[url + ":filename"]):
        send_to_minio(url, meta_urls, current_folder)
    else:
        logging.warning(meta_urls[url + ":filename"] + " is badly structured, deleting...")
        os.remove(current_folder + "/" + meta_urls[url + ":filename"])
        log_and_send_error(meta_urls[url + ":filename"])


def remove_and_create_folder(folder_path: str, toCreate: bool) -> None:
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    if toCreate:
        os.makedirs(folder_path)


def check_if_data_available(batches: list, url: str) -> list:
    try:
        r = meteo_client.get(url, timeout=10)
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


def get_latest_theorical_batches(ctx: str) -> tuple[list, dict]:
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
                )
    return batches, tested_batches


def does_file_exist_in_minio(file: str, bucket: str = MINIO_BUCKET) -> bool:
    try:
        client.stat_object(bucket, file)
        return True
    except S3Error as e:
        if e.code == "NoSuchKey":
            return False
        else:
            raise


def construct_all_possible_files(
    batches: list,
    tested_batches: dict
) -> tuple[dict, dict]:
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

    to_get = [
        f for f in minio_paths
        if not does_file_exist_in_minio(f)
    ]

    logging.info(
        str(len(to_get))
        + " possible file(s) after removing already processed files"
    )

    if len(to_get) == 0:
        logging.info("no new data, exit")
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

    return meta_urls, family_batches


def process_urls(
    family_batches: dict,
    meta_urls: dict,
    current_folder: str,
    max_workers: int,
    delay_between_batches: int,
    start: int,
) -> None:
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
                    # logging.info(fb + " " + len(family_batches[fb][i]))
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
            _ = [
                executor.submit(process_url, url, meta_urls, current_folder)
                for url in batch
            ]

            # Pause d'une minute entre les paquets
            if batch_nb != max_iter:
                time.sleep(delay_between_batches)


def processing_each_possible_files(
    meta_urls: dict,
    current_folder: str,
    family_batches: dict,
) -> None:

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


def reorder_resources(ctx: str) -> None:
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


def clean_old_runs_in_minio(batches: list) -> None:
    # we get the run's names from the folders
    get_list_runs = get_files_from_prefix(
        prefix="pnt/",
        recursive=False,
    )

    old_dates = []
    keep_dates = []
    for run in get_list_runs:
        # run.object_name looks like "pnt/2024-10-02T00:00:00Z/"
        run = run.object_name.split('/')[1]
        if (
            run < batches[-1]
            and run not in old_dates
        ):
            old_dates.append(run)

        if (
            run >= batches[-1]
            and run not in keep_dates
        ):
            keep_dates.append(run)

    if len(keep_dates) > 3:
        for od in old_dates:
            delete_files_prefix(
                prefix="pnt/" + od
            )


def get_package_from_name(name: str) -> tuple[str, Optional[str], str]:
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


def get_params(name: str, detail: Optional[str], grille: str):
    for p in PACKAGES:
        if p['type_package'] == name and p['grid'] == grille:
            if detail is None:
                return p
            elif p['detail_package'] == detail:
                return p
    raise Exception('Should not happen')


def publish_on_datagouv(current_folder: str, ctx: str) -> bool:
    reorder = False
    get_list_files_updated = get_latest_files_from_package(ctx)
    minio_files = {}
    # re-getting minio files as they have been updated
    # only for the current package type
    logging.info("Getting minio files...")
    for minio_path in get_list_files_updated:
        name = "__".join(
            minio_path.split("/")[-1].split(".")[0].split("__")[:-1]
        )
        date_file = minio_path.split("/")[-1].split(".")[0].split("__")[-1]
        if name not in minio_files or minio_files[name]['date'] < date_file:
            minio_files[name] = {'date': date_file, 'path': minio_path}

    # getting files currently on data.gouv
    logging.info("Getting data.gouv files...")
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

    logging.info("Synchronizing...")
    for name in minio_files:
        # skipping if not the current package type
        if get_package_from_name(name)[0] not in ctx.split(","):
            continue
        # if the file is already on data.gouv and it's more recent on minio => upload
        if name in datagouv_files:
            if minio_files[name]['date'] > datagouv_files[name]['date']:
                logging.info(f"{name}: updating on data.gouv.fr...")
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
                        "=> Succesfully updated on data.gouv.fr "
                        f"({datagouv_files[name]['date']} => "
                        f"{minio_files[name]['date']})"
                    )
        else:
            logging.info(f"{name}: creating on data.gouv.fr...")
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
                logging.info("=> Successfully created in data.gouv.fr")

    return reorder
