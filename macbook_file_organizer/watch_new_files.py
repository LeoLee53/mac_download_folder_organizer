import concurrent.futures
import os.path
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import move_files


class FileAddedHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    # def on_modified(self, event):
    #     self.pool.submit(move_files.move_file, event.src_path)

    def on_created(self, event):
        basename = os.path.basename(event.src_path)
        can_do = ((not event.is_directory) or
                  not (basename.startswith('*') and basename.endswith('*')))

        if can_do:
            self.pool.submit(move_files.move_file, event.src_path)


observer = Observer()
handler = FileAddedHandler()
observer.schedule(handler, path=move_files.DOWNLOAD_FOLDER_PATH, recursive=False)

observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
