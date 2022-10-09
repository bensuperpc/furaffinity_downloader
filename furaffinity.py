#!/usr/bin/env python

from requests.cookies import RequestsCookieJar
from concurrent.futures import ProcessPoolExecutor
import concurrent
from itertools import count
import argparse
import time
import os

from loguru import logger
from random import randint
from dotenv import load_dotenv
import faapi


class FurAffinity:
    def __init__(self, **kwargs):

        kwargs.setdefault("cookies", None)
        kwargs.setdefault("a_cookies", None)
        kwargs.setdefault("b_cookies", None)
        kwargs.setdefault("thread_worker", 32)
        kwargs.setdefault("output_dir", None)

        # for key, val in kwargs.items():
        #    self.__dict__[key] = val

        logger.info("Initializing FurAffinity")

        self.thread_worker = kwargs["thread_worker"]

        if kwargs["output_dir"] is None:
            self.output_dir = os.getcwd()
        else:
            self.output_dir = kwargs["output_dir"]

        self.set_cookies(kwargs["cookies"],
                         kwargs["a_cookies"], kwargs["b_cookies"])
        logger.info("FurAffinity initialized")

    # Define cookies for the session
    def set_cookies(self, cookies: RequestsCookieJar = None, a_cookies: str = None, b_cookies: str = None):

        if cookies and a_cookies and b_cookies:
            logger.warning(
                "Cookies and a_cookies/b_cookies are mutually exclusive. Using cookies.")

        if cookies:
            logger.info("Using provided cookies")
            self.cookies = cookies
            self.api = faapi.FAAPI(self.cookies)

        elif a_cookies and b_cookies:
            logger.info("Using provided a and b cookies")
            self.cookies = RequestsCookieJar()
            self.cookies.set("a", a_cookies)
            self.cookies.set("b", b_cookies)
            self.api = faapi.FAAPI(self.cookies)

        else:
            logger.warning("No cookies provided, using default")
            self.cookies = RequestsCookieJar()
            self.api = faapi.FAAPI(self.cookies)

    # Download submissions from ID
    def download_submission(self, subID: int, wait_time: bool = True, retry_time: int = 5, retry_count: int = 3):

        # To avoid getting errors from the server due to massive downloading, we wait a random amount of time (100-10000ms)
        if wait_time:
            time.sleep(randint(100, 10000)/1000)

        for _ in range(retry_count):
            try:
                sub, sub_file = self.api.submission(
                    subID, get_file=True, chunk_size=None)

                if sub is None or sub_file is None:
                    logger.warning(f"Submission {subID} is not found")
                    return

                logger.debug(
                    f"Downloading {sub.id} {sub.title} {sub.author} {(len(sub_file) / 1024):.3f}KiB")

                output_file = os.path.join(
                    self.output_dir, sub.file_url.split('/')[-1])
                logger.debug(f"Writting {output_file}")

                # os.makedirs(self.output_dir, exist_ok=True)

                with open(sub.file_url.split("/")[-1], "wb") as f:
                    f.write(sub_file)

                break
            except Exception as e:
                logger.error(e)
                logger.warning(f"Retrying {subID}")
                time.sleep(retry_time)
                continue
            else:
                logger.debug(f"Successfully downloaded {subID}")
                break
        else:
            logger.error(f"Failed to download {subID}")
            return

    # Get submission IDs from artist from gallery
    def get_all_gallery_submission_id(self, user):
        submissionIDs = []

        logger.info(f"Getting submission IDs of {user} from gallery")
        for i in count(0):
            gallery, _ = self.api.gallery(user=user, page=i)
            if gallery is None or len(gallery) == 0:
                break
            logger.debug(f"Page {i} has {len(gallery)} submissions")
            for submission in gallery:
                submissionIDs.append(submission.id)

        logger.debug(f"Total {len(submissionIDs)} submissions")
        return submissionIDs

    # Get submission IDs from artist from scraps
    def get_all_scraps_submission_id(self, user):
        submissionIDs = []

        logger.info(f"Getting submission IDs of {user} from scraps")
        for i in count(0):
            scraps, _ = self.api.scraps(user=user, page=i)
            if scraps is None or len(scraps) == 0:
                break
            logger.debug(f"Page {i} has {len(scraps)} submissions")
            for submission in scraps:
                submissionIDs.append(submission.id)

        logger.debug(f"Total {len(submissionIDs)} submissions")
        return submissionIDs

    # ThreadPool to download in parallel
    def thread_pool(self, func: callable, args: list, max_workers: int = None, in_order: bool = False):

        if max_workers is None:
            max_workers = self.thread_worker
        else:
            self.thread_worker = max_workers

        if in_order:
            logger.warning("In order is not tested yet")

        results = []
        with ProcessPoolExecutor(max_workers=self.thread_worker) as executor:
            futures = None
            if in_order:
                futures = executor.map(func, args)
            else:
                futures = list(executor.submit(func, item)
                               for item in args)
                #futures = list(map(lambda x: executor.submit(func, x), args))

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        return results

    def download_gallery(self, user):

        logger.info(f"Downloading gallery of {user}")

        self.thread_pool(self.download_submission, self.get_all_gallery_submission_id(
            user), max_workers=32, in_order=False)

        logger.info(f"Finished downloading gallery of {user}")


if __name__ == "__main__":

    # Load .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    COOKIE_A = os.environ.get("COOKIE_A", None)
    COOKIE_B = os.environ.get("COOKIE_B", None)

    if COOKIE_A is None or COOKIE_B is None:
        logger.error("No a and b cookies specified")
        exit(1)

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

    furAffinity = FurAffinity(
        a_cookies=COOKIE_A, b_cookies=COOKIE_B, thread_worker=args.jobs)

    for artist in artists:
        furAffinity.download_gallery(artist)
