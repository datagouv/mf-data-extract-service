from datetime import datetime
import logging
import time
import sys

from utils import (
    clean_old_runs_in_minio,
    construct_all_possible_files,
    get_latest_theorical_batches,
    processing_each_possible_files,
    publish_on_datagouv,
    remove_and_create_folder,
    reorder_resources,
)

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    while True:
        
        logging.info("-------------------------------------")
        logging.info(f"------  NEW PROCESS {datetime.now().strftime('%Y-%m-%dT%H:%M')}  ------")
        logging.info("-------------------------------------")

        result = None
        list_files = None
        meta_urls = None
        family_batches = None
        get_list_files = None

        ctx = sys.argv[1]
        current_folder = "./data" + "-" + ctx.replace(",", "-")

        logging.info("---- Remove and create local data folder ----")
        remove_and_create_folder(current_folder, True)

        logging.info("---- Get latest theorical batches -----")
        batches, tested_batches = get_latest_theorical_batches(ctx)

        logging.info("---- Construct all possibles files ----")
        try:
            result = construct_all_possible_files(batches, tested_batches)
        except TypeError as e:
            result = None
            logging.info("Error - wait next batch")

        if result is not None:
            list_files, meta_urls, family_batches, get_list_files = result

        try:
            logging.info("---- Processing each possible files ----")
            processing_each_possible_files(meta_urls, current_folder, family_batches)
        except:
            logging.info("EXCEPTION")
            pass

        try:
            logging.info("---- Publish all new files in data.gouv.fr ----")
            reorder = publish_on_datagouv(current_folder, ctx)
            
            if reorder: 
                logging.info("---- Reorder resources of data.gouv for each dataset ----")
                reorder_resources(ctx)
        except:
            logging.info("Problem occurs during publishing in data.gouv")
            pass

        logging.info("---- Remove files in minio and data.gouv.fr if more than MAX BATCH SIZE ----")
        clean_old_runs_in_minio(batches)

        logging.info("---- Delete local data folder ----")
        remove_and_create_folder(current_folder, False)

        logging.info("------       END PROCESS       ------")
        logging.info("-")

        time.sleep(60)
