import requests
from datetime import datetime, timedelta
import random
import time
import sys

from config import PACKAGES, MAX_LAST_BATCHES, MINIO_BUCKET, MINIO_PASSWORD, MINIO_URL, MINIO_USER, APIKEY_DATAGOUV, DATAGOUV_URL
from utils import get_last_batch_hour, process_urls, delete_files_prefix, remove_and_create_folder, check_if_data_available

if __name__ == "__main__":
    print("---- Remove and create local data folder ----")
    current_folder = "./data-" + datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    remove_and_create_folder(current_folder, True)

    print("---- Get already processed files ----")
    res_list = []
    processed_files = []
    for package in PACKAGES:
        print(package['dataset_id'])
        r = requests.get(f"{DATAGOUV_URL}/api/1/datasets/{package['dataset_id']})
        data = r.json()
        for res in data["resources"]:
            if "latest" not in res["title"]:
                processed_files.append(res["title"])

    print("---- Get latest theorical batches -----")
    batches = []
    for i in range(MAX_LAST_BATCHES):
        batches.append((get_last_batch_hour() - timedelta(hours=6*i)).strftime("%Y-%m-%dT%H:%M:%SZ"))

    print(batches)
    tested_batches = {}
    tested_batches["arpege"] = check_if_data_available(batches, "arpege")
    tested_batches["arome"] = check_if_data_available(batches, "arome")

    print("---- Construct all possibles files ----")
    list_files = []
    meta_urls = {}
    for batch in batches:
        for family_package in PACKAGES:
            if batch in tested_batches[family_package["type_package"]]:
                for package in family_package["packages"]:
                    for timeslot in package["time"]:
                        headers = {"Content-Type": "application/json; charset=utf-8", "apikey": family_package["apikey"] }
                        url = (
                            family_package["base_url"] + "/" + family_package["grid"] + \
                            "/packages/" + package["name"] + "/" + family_package["product"] + \
                            "?&referencetime=" + batch + "&time=" + timeslot + "&format=grib2" 
                        )
                        filename = (
                            family_package["type_package"] + "__" + family_package["grid"].replace("0.", "0") + \
                            "__" + package["name"] + "__" + timeslot + "__" + batch + ".grib2"
                        )
                        list_files.append(filename)
                        meta_urls[url+":headers"] = headers
                        meta_urls[url+":filename"] = filename                    
                        meta_urls[filename+":url"] = url


    print(str(len(list_files)) + " possible files")

    to_get = list(set(list_files) - set(processed_files))

    print(str(len(to_get)) + " possible files after removing already processed files")


    to_get_url = []
    for tg in to_get:
        to_get_url.append(meta_urls[tg+":url"])

    # Remplacez ceci par votre tableau d'URL


    if len(to_get) == 0:
        print("---- no new data ----")
        sys.exit()

    print("---- Shuffle and process batch of 50 files ----")
    random.shuffle(to_get_url)

    start = time.time()

    max_workers = 200  # Nombre maximal de requêtes simultanées
    delay_between_batches = 60  # Délai en secondes entre les paquets

    process_urls(to_get_url, meta_urls, max_workers, delay_between_batches, start)
    end = time.time()
    print(end - start)


    print("---- Get data.gouv API to retrieve list of new data ----")
    res_list = []
    type_res = {}
    latest_res = {}
    did_res = {}
    for package in PACKAGES:
        print(package['dataset_id'])
        r = requests.get(f"{DATAGOUV_URL}/api/1/datasets/{package['dataset_id']})
        data = r.json()
        for res in data["resources"]:
            res_list.append({"title": res["title"], "id": res["id"], "did": package["dataset_id"]})
            if "latest" not in res["title"]:
                if "__".join(res["title"].split("__")[:4]) not in type_res:
                    type_res["__".join(res["title"].split("__")[:4])] = [res["title"].split("__")[4].split(".")[0]]
                else:
                    type_res["__".join(res["title"].split("__")[:4])].append(res["title"].split("__")[4].split(".")[0])
            else:
                latest_res["__".join(res["title"].split("__")[:4])] = res["id"]
            did_res["__".join(res["title"].split("__")[:4])] = package["dataset_id"]

    print("---- Create or Replace latest files in data.gouv ----")
    for item in type_res:
        body = {
            "title": item + "__" + max(type_res[item]) + "__latest.grib2",
            'url': (
                f"https://{MINIO_URL}/{MINIO_BUCKET}/pnt/" + \
                max(type_res[item]) + "/" + \
                item.split("__")[0] + "/" + \
                item.split("__")[1] + "/" + \
                item.split("__")[2] + "/" + \
                item + "__" + max(type_res[item]) + ".grib2"
            ),
            'filetype': 'remote'
        }
        if item in latest_res:
            # put
            r = requests.put(f"{DATAGOUV_URL}/api/1/datasets/{did_res[item]}/resources/{latest_res[item]}/", json=body, headers={"X-API-KEY": APIKEY_DATAGOUV})

        else:
            # post
            r = requests.post(f"{DATAGOUV_URL}/api/1/datasets/{did_res[item]}/resources/", json=body, headers={"X-API-KEY": APIKEY_DATAGOUV})

    print("---- Delete old resources of data.gouv.fr for each dataset ----")
    res_list = []
    for package in PACKAGES:
        print(package['dataset_id'])
        r = requests.get(f"{DATAGOUV_URL}/api/1/datasets/" + package["dataset_id"])
        data = r.json()
        for res in data["resources"]:
            if res["title"].split("__")[4].split(".")[0] < min(batches): 
                print("delete : " + res["title"])
                r = requests.delete(f"{DATAGOUV_URL}/api/1/datasets/{package['dataset_id']}/resources/{res['id']}/", json=body, headers={"X-API-KEY": APIKEY_DATAGOUV})
        print(r.status_code)

    print("---- Reorder resources of data.gouv for each dataset ----")
    res_list = []
    for package in PACKAGES:
        print(package['dataset_id'])
        r = requests.get(f"{DATAGOUV_URL}/api/1/datasets/" + package["dataset_id"])
        data = r.json()
        for res in data["resources"]:
            res_list.append({"title": res["title"], "id": res["id"], "did": package["dataset_id"]})
        sorted_data = sorted(res_list, key=lambda x: x['title'])
        body = [{"id": x["id"]} for x in sorted_data]
        r = requests.put(f"{DATAGOUV_URL}/api/1/datasets/{package['dataset_id']}/resources/", json=body, headers={"X-API-KEY": APIKEY_DATAGOUV})
        print(r.status_code)


    print("---- Remove files in minio and data.gouv.fr if more than MAX BATCH SIZE ----")
    processed_files_clean = []
    folders_to_remove = []
    for pf in processed_files:
        if min(batches) > pf.split("__")[4].split(".")[0]:
            print(pf.split("__")[4].split(".")[0])
            folders_to_remove.append(pf.split("__")[4].split(".")[0])
        else:
            processed_files_clean.append(pf)
    folders_to_remove = list(set(folders_to_remove))

    for folder in folders_to_remove:
        delete_files_prefix(
            MINIO_URL=MINIO_URL,
            MINIO_BUCKET=MINIO_BUCKET,
            MINIO_USER=MINIO_USER,
            MINIO_PASSWORD=MINIO_PASSWORD,
            prefix="pnt/"+folder
        )

    print("---- Delete local data folder ----")
    remove_and_create_folder(current_folder, False)
