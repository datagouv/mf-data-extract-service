import boto3
import botocore
from minio import Minio, S3Error
from typing import List, TypedDict, Optional
import os
from datetime import datetime
import requests
import concurrent.futures
import time
import shutil

from config import MINIO_BUCKET, MINIO_URL, MINIO_USER, MINIO_PASSWORD, PACKAGES, APIKEY_DATAGOUV, BATCH_URL_SIZE


class File(TypedDict):
    source_path: str
    source_name: str
    dest_path: str
    dest_name: str
    content_type: Optional[str]


def send_files(
    MINIO_URL: str,
    MINIO_BUCKET: str,
    MINIO_USER: str,
    MINIO_PASSWORD: str,
    list_files: List[File]
):
    """Send list of file to Minio bucket

    Args:
        MINIO_URL (str): Minio endpoint
        MINIO_BUCKET (str): bucket
        MINIO_USER (str): user
        MINIO_PASSWORD (str): password
        list_files (List[File]): List of Dictionnaries containing for each
        `source_path` and `source_name` : local file location ;
        `dest_path` and `dest_name` : minio location (inside bucket specified) ;

    Raises:
        Exception: when specified local file does not exists
        Exception: when specified bucket does not exist
    """
    client = Minio(
        MINIO_URL,
        access_key=MINIO_USER,
        secret_key=MINIO_PASSWORD,
        secure=True,
    )
    found = client.bucket_exists(MINIO_BUCKET)
    if found:
        for file in list_files:
            is_file = os.path.isfile(
                os.path.join(file["source_path"], file["source_name"])
            )
            if is_file:
                dest_path = f"{file['dest_path']}{file['dest_name']}"
                print("Sending " + file["source_path"] + file["source_name"])
                print("to " + dest_path)
                client.fput_object(
                    MINIO_BUCKET,
                    dest_path,
                    os.path.join(file["source_path"], file["source_name"]),
                    content_type=file['content_type'] if 'content_type' in file else None
                )
            else:
                raise Exception(
                    f"file {file['source_path']}{file['source_name']} "
                    "does not exists"
                )
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
        secure=True,
    )
    found = client.bucket_exists(MINIO_BUCKET)
    
    try:
        # List objects in the specified folder
        objects = client.list_objects(MINIO_BUCKET, prefix=prefix, recursive=True)

        # Create a list of object names to delete
        objects_to_delete = [obj.object_name for obj in objects]

        # Delete all objects in the folder
        for obj_name in objects_to_delete:
            client.remove_object(MINIO_BUCKET, obj_name)

        print(f"All objects with prefix '{prefix}' deleted successfully.")

    except S3Error as e:
        print(f"Error: {e}")


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
    batch_time = (now.replace(second=0, microsecond=0, minute=0, hour=batch_hour))
    return batch_time


def download_url(url, meta_urls, retry):
    if retry != 0:
        if retry != 5: print("Retry " + str(5-retry) + "for " + url)
        try:
            print(url)
            filename = meta_urls[url + ":filename"]
            headers = meta_urls[url + ":headers"]

            with requests.get(url, stream=True, headers=headers, timeout=60) as r:
                r.raise_for_status()
                with open("data/" + filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=32768): 
                        f.write(chunk)

        except Exception as e:
            download_url(url, meta_urls, retry-1)
    else:
        print(f"----- EXCEPTION: {url} ------")


def send_to_minio(url, meta_urls):
    send_files(
        MINIO_URL=MINIO_URL,
        MINIO_BUCKET=MINIO_BUCKET,
        MINIO_USER=MINIO_USER,
        MINIO_PASSWORD=MINIO_PASSWORD,
        list_files=[
            {
                "source_path": "data/",
                "source_name": meta_urls[url + ":filename"],
                "dest_path": (
                    "pnt/" + url.split("referencetime=")[1].split("&")[0] + "/" + \
                    meta_urls[url + ":filename"].split("__")[0] + "/" + \
                    meta_urls[url + ":filename"].split("__")[1] + "/" + \
                    meta_urls[url + ":filename"].split("__")[2] + "/"
                ),
                "dest_name": meta_urls[url + ":filename"],
                "content_type": meta_urls[url + ":filename"] 
            }
        ],
    )
    print(f"sent to minio: {url}")
    

def sent_to_datagouv(url, meta_urls):
    body = {
        "title": meta_urls[url + ":filename"],
        'url': (
            f"https://{MINIO_URL}/{MINIO_BUCKET}/pnt/" + \
            url.split("referencetime=")[1].split("&")[0] + "/" + \
            meta_urls[url + ":filename"].split("__")[0] + "/" + \
            meta_urls[url + ":filename"].split("__")[1] + "/" + \
            meta_urls[url + ":filename"].split("__")[2] + "/" + \
            meta_urls[url + ":filename"]
        ),
        'filetype': 'remote'
    }
    did = None
    for package in PACKAGES:
        if(
            (package["type_package"] == meta_urls[url + ":filename"].split("__")[0]) & 
            (package["grid"].replace("0.", "0") == meta_urls[url + ":filename"].split("__")[1].replace("0.", "0"))
        ):
            did = package["dataset_id"]
    print("did" + str(did))
    if did:
        r = requests.post(f"https://demo.data.gouv.fr/api/1/datasets/{did}/resources/", json=body, headers={"X-API-KEY": APIKEY_DATAGOUV})
        print(r.status_code)
        print(r.json())
        print(f"url {url} ok in data.gouv.fr")
            
        
def process_url(url, meta_urls):
    download_url(url, meta_urls, 5)
    send_to_minio(url, meta_urls)
    sent_to_datagouv(url, meta_urls)

    
def process_urls(urls, meta_urls, max_workers, delay_between_batches, start):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Divisez les URL en paquets de X
        url_batches = [urls[i:i+BATCH_URL_SIZE] for i in range(0, len(urls), BATCH_URL_SIZE)]

        for batch in url_batches:
            end = time.time()
            print(end - start)
            # Lancez les requêtes pour chaque URL dans le paquet simultanément
            futures = [executor.submit(process_url, url, meta_urls) for url in batch]
            # Attendez que toutes les requêtes dans le paquet soient terminées
            #concurrent.futures.wait(futures)

            # Pause d'une minute entre les paquets
            if len(batch) == BATCH_URL_SIZE:
                time.sleep(delay_between_batches)


def remove_and_create_folder(folder_path, toCreate):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' removed.")

    if toCreate:
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")


def check_if_data_available(batches, type_package):
    if type_package == "arpege"
        r = requests.get("https://public-api.meteofrance.fr/previnum/DPPaquetARPEGE/models/ARPEGE/grids/0.25/packages/IP1")
    else:
        r = requests.get("https://public-api.meteofrance.fr/previnum/DPPaquetARPEGE/models/ARPEGE/grids/0.25/packages/IP1")

    new_batches = []
    try:
        if "links" in r.json():
            for batch in batches:
                for link in r.json()["links"]:
                    if batch in link["href"]:
                        new_batches.append(batch)
        return new_batches
    except:
        print("--- ERROR API ----")