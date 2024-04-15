import os.path
import time

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

import move_files
from delete_file import _is_category_folder


class NewDownloadHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_created(self, event: FileSystemEvent) -> None:
        basename = os.path.basename(event.src_path)

        can_do = (not event.is_directory and
                  not basename.endswith('.crdownload') and
                  not basename.startswith('.'))

        if can_do:
            move_files.move_file(event.src_path)

    def on_moved(self, event: FileSystemEvent) -> None:
        dest_dir_name = os.path.dirname(event.dest_path).split('/')[-1]
        if _is_category_folder(dest_dir_name):
            return

        src_dir_name = os.path.dirname(event.src_path).split('/')[-1]
        if src_dir_name.endswith('.download'):
            move_files.move_file(event.dest_path)


observer = Observer()
handler = NewDownloadHandler()
observer.schedule(handler, path=move_files.DOWNLOAD_FOLDER_PATH, recursive=False)

observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
