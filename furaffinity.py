#!/usr/bin/env python

from requests.cookies import RequestsCookieJar
from concurrent.futures import ProcessPoolExecutor
from itertools import count
import argparse
import time
import os

from loguru import logger
from random import randint
from dotenv import load_dotenv
import faapi


def download(subID, api):
    # To avoid getting errors from the server, we wait a random amount of time (100-10000ms)
    time.sleep(randint(100, 10000)/1000)

    retry_time = 20
    time_between_retry = 5

    for _ in range(retry_time):
        try:
            sub, sub_file = api.submission(
                subID, get_file=True, chunk_size=512 * 1024)
            logger.debug(
                f"Downloading {sub.id} {sub.title} {sub.author} {(len(sub_file) / 1024):.3f}KiB")
            logger.debug(f"Writting {sub.file_url.split('/')[-1]}")
            with open(sub.file_url.split("/")[-1], "wb") as f:
                f.write(sub_file)
            break
        except Exception as e:
            logger.error(e)
            logger.warning(f"Retrying {subID}")
            time.sleep(time_between_retry)
            continue
        else:
            logger.debug(f"Successfully downloaded {subID}")
            break
    else:
        logger.error(f"Failed to download {subID}")
        return


if __name__ == "__main__":
    # Load .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Download submissions from FurAffinity')
    parser.add_argument('-a', '--artists', nargs='+',
                        default=[], help='Artists to download from')
    parser.add_argument('-j', '--jobs', type=int, default=32,
                        help="Number of parallel downloads")

    args = parser.parse_args()
    artists = args.artists

    if not artists:
        logger.error("No artists specified")
        exit(1)

    logger.debug(f"Downloading from {artists}")
    logger.debug(f"Using {args.jobs} jobs")

    cookies = RequestsCookieJar()

    COOKIE_A = os.environ.get("COOKIE_A", None)
    COOKIE_B = os.environ.get("COOKIE_B", None)

    if COOKIE_A is None or COOKIE_B is None:
        logger.error("No cookies specified")
        exit(1)

    cookies.set("a", str(COOKIE_A))
    cookies.set("b", str(COOKIE_B))

    api = faapi.FAAPI(cookies)

    submissionIDs = []

    for artist in artists:
        logger.debug(f"Getting submissions from {artist}")
        for i in count(0):
            gallery, _ = api.gallery(user=artist, page=i)
            if gallery is None or len(gallery) == 0:
                break
            logger.debug(f"Page {i} has {len(gallery)} submissions")
            for submission in gallery:
                submissionIDs.append(submission.id)
    logger.debug(f"Total {len(submissionIDs)} submissions")

    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        start = time.perf_counter()

        # download all submissions in parallel
        futures = [executor.submit(download, item, api)
                   for item in submissionIDs]

        # Wait for all threads to finish
        for future in futures:
            future.result()

        finish = time.perf_counter()
        logger.debug(f"Finished in {round(finish-start, 2)} second(s)")
