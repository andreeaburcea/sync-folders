# Problem 2

import sys
import time
import os
import logging
from dirsync import sync
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


source = input('Enter your path for source folder: ')
replica = input('Enter your path for replica folder: ')

LOG = 'log.txt'
now_time = None
old_time = None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=LOG)
    logging.info(sys.stdout)
    logger = logging.getLogger('')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            now_time = os.path.getmtime(source)
            if now_time != old_time:
                folder_sync = sync(source, replica, 'sync', verbose=True, purge=True, ctime=True, logger=logger)
                old_time = now_time
                time.sleep(1)
                if sys.stdout:
                    with open(LOG, 'a') as message:
                        message.write(f'Modified {source} {replica} \n')
                    time.sleep(1)
                    #break

    finally:
        observer.stop()
        observer.join()