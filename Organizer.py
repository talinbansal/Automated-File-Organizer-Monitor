## --------------------------------------------- Imports --------------------------------------------- ##
import os
import time
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

## ------------------------------------------------ Constants ------------------------------------------------ ##
main_directory = '/Users/talinbansal/Desktop'
pdf_path = '/Users/talinbansal/Desktop/pdf_folder'
img_path = '/Users/talinbansal/Desktop/img_folder'
mp4_path = '/Users/talinbansal/Desktop/video_folder'

destination_directory = {
    '.jpg': img_path,
    '.png': img_path,
    '.jpeg': img_path,
    '.heic': img_path,
    '.pdf': pdf_path,
    '.mp4': mp4_path,
    '.mov': mp4_path
}

## ------------------------------------------------ Moving & Deleting Files ------------------------------------------------ ##
def move_file(file, destination):
    try:
        shutil.copy2(file, destination)
        os.remove(file)
        logging.info(f'Moved {file} to {destination}')
    except Exception as e:
        logging.error(f'Error processing file {file}: {e}')
        

def handle_existing_files():
    with os.scandir(main_directory) as entries:
        for entry in entries:
            file = entry.path
            name = entry.name 
            if entry.is_file():
                _, ext = os.path.splitext(name)
                if ext.lower() in destination_directory:
                    move_file(file, os.path.join(destination_directory[ext.lower()], name))
                    
## Deals with New Files 
class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            _, ext = os.path.splitext(event.src_path)
            event_name = os.path.basename(event.src_path)
            if ext.lower() in destination_directory:
                move_file(event.src_path, os.path.join(destination_directory[ext.lower()], event_name))
            
## ------------------------------------------------ Watchdog API ------------------------------------------------ ##
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handle_existing_files()  # Handle existing files in the directory
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, main_directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()