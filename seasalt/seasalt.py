import importlib
import os
import sys
from p_tqdm import p_map
from tqdm import tqdm

import globals

BATCH_SIZE = 10
NUM_WORKERS = 16


def lazy_import(name):
    spec = importlib.util.find_spec(name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


def scrape_one(param):
    if globals.SHOULD_CANCEL:
        globals.IS_DOWNLOADING = False
        globals.SHOULD_CANCEL = False
        return "Cancelled"
    try:
        scraper, saver, url, parallel, scraper_args, saver_args = param
        image, meta = scraper.get_post(url, parallel, scraper_args)
        if image and meta:
            saver.save(image, meta, saver_args)
    except Exception as e:
        print(e)


def cancel():
    if globals.IS_DOWNLOADING:
        print('Attempting to cancel...')
        globals.SHOULD_CANCEL = True
    else:
        print('Nothing to cancel')


def download(scraper_module, url, parallel_dl, limit):
    if not os.path.isdir(globals.PROJECT_DIRECTORY):
        return 'Project directory not found! Make sure to set it in the config!'
    scraper_args = []
    saver_args = [globals.PROJECT_DIRECTORY]
    globals.IS_DOWNLOADING = True
    print(globals.IS_DOWNLOADING)

    limit = int(limit)
    scraper = lazy_import('seasalt.modules.scrapers.' + scraper_module)
    saver = lazy_import('seasalt.modules.saver.' + 'folder')

    scraper = scraper.Scraper()
    saver = saver.Saver()

    if limit == -1:
        limit = float('inf')

    if not parallel_dl:
        cur_url = url
        to_scrape = scraper.get_posts(cur_url, parallel_dl, scraper_args)
        if to_scrape:
            while True:
                while to_scrape:
                    if globals.SHOULD_CANCEL:
                        globals.IS_DOWNLOADING = False
                        globals.SHOULD_CANCEL = False
                        return "Cancelled"
                    scrape_one((scraper, saver, to_scrape.pop()))
                cur_url = scraper.next_page(cur_url, parallel_dl, scraper_args)
                if not cur_url:
                    break
                print('Navigating to', cur_url)
                to_scrape = scraper.get_posts(cur_url, parallel_dl, scraper_args)
        else:
            print('No posts found!')
        print('Finished!')
    else:
        cont = True
        cur_url = url
        urls = []
        downloaded = 0
        while not globals.SHOULD_CANCEL:
            tqdm.write('Loading batch...')
            for _ in tqdm(range(BATCH_SIZE)):
                if globals.SHOULD_CANCEL:
                    globals.IS_DOWNLOADING = False
                    globals.SHOULD_CANCEL = False
                    return "Cancelled"
                if not cont:
                    break
                new_urls = scraper.get_posts(cur_url, parallel_dl, scraper_args)
                urls += new_urls
                cur_url = scraper.next_page(cur_url, parallel_dl, scraper_args)
                if len(urls) > limit:
                    cont = False
                if not cur_url:
                    cont = False

            tqdm.write('Downloading batch...')
            tasks = [(scraper, saver, url, parallel_dl, scraper_args, saver_args) for url in urls]
            if downloaded + len(tasks) > limit:
                tasks = tasks[:limit - downloaded]
                cont = False
            p_map(scrape_one, tasks, **{"num_cpus": NUM_WORKERS})
            downloaded += len(tasks)
            if not cont:
                break
            urls = []
    globals.IS_DOWNLOADING = False
    return "Download Finished!"
