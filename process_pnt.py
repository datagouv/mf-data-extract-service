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
cooldown = 60


if __name__ == "__main__":
    while True:

        logging.info("--------------------------------------")
        logging.info(f"---  NEW PROCESS {datetime.now().strftime('%Y-%m-%dT%H:%M')}  ---")
        logging.info("--------------------------------------")

        result = None
        list_files = None
        meta_urls = None
        family_batches = None
        get_list_files = None
        skip = False

        ctx = sys.argv[1]
        current_folder = "./data" + "-" + ctx.replace(",", "-")

        logging.info("---- Remove and create local data folder ----")
        remove_and_create_folder(current_folder, True)

        logging.info("---- Get latest theorical batches -----")
        batches, tested_batches = get_latest_theorical_batches(ctx)

        logging.info("---- Construct all possible files ----")
        try:
            result = construct_all_possible_files(batches, tested_batches)
        except TypeError as e:
            result = None
            logging.warning(f"Error constructing files: {e}")
            logging.info(f"Restarting a process in {cooldown}s")
            time.sleep(cooldown)
            continue

        if result is not None:
            meta_urls, family_batches = result
        else:
            skip = True

        if not skip:
            try:
                logging.info("---- Processing each possible file ----")
                processing_each_possible_files(meta_urls, current_folder, family_batches)
            except Exception as e:
                logging.warning(f"Error processing all file combinations: {e}")
                logging.info(f"Restarting a process in {cooldown}s")
                time.sleep(cooldown)
                continue

        try:
            logging.info("---- Publish all new files in data.gouv.fr ----")
            reorder = publish_on_datagouv(current_folder, ctx)

            if reorder:
                logging.info("---- Reorder resources of data.gouv for each dataset ----")
                reorder_resources(ctx)
        except Exception as e:
            logging.warning(f"Problem occured during publishing in data.gouv: {e}")
            logging.info(f"Restarting a process in {cooldown}s")
            time.sleep(cooldown)
            continue

        logging.info("---- Remove files in minio and data.gouv.fr if more than MAX BATCH SIZE ----")
        clean_old_runs_in_minio(batches)

        logging.info("---- Delete local data folder ----")
        remove_and_create_folder(current_folder, False)

        logging.info("------       END PROCESS       ------")
        logging.info("-")

        time.sleep(cooldown)
