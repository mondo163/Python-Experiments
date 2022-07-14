from concurrent.futures import thread
from threading import Thread, currentThread
import threading
import time
from tracemalloc import start
import requests
from pathlib import Path
from eliot import start_action, to_file, preserve_context
to_file(open("D:\Repositories\Work-Experiments\Logs\outputThread.log", "w"))

DOWNLOAD_FOLDER =Path("D:\\Repositories\\Work-Experiments\\Downlaods")
ISO_FILE="https://cdimage.debian.org/cdimage/archive/9.13.0/amd64/iso-cd/debian-9.13.0-amd64-netinst.iso"
def GetIsoFile(filename: str):
    with start_action(action_type=f"Getting {filename}: Started at {time.strftime('%X')}", currentThread=threading.get_ident()) as action:
        resp = requests.api.get(ISO_FILE)
        if resp.status_code == 200:
            open((DOWNLOAD_FOLDER/filename).with_suffix(".iso"), "wb").write(resp.content)
        action.log(message_type=f"Completed getting {filename} at {time.strftime('%X')}", thread=Thread.__name__)


def main():
    """ task = []
    with start_action(action_type="creating tasks:") as action:
       task1 = asyncio.create_task()
       action.log(message_type="Task 1 created", thread=task1.get_name())
       task2 = asyncio.create_task(GetIsoFile("file2"))
       action.log(message_type="Task 2 created", thread=task2.get_name())
       task3  = asyncio.create_task(GetIsoFile("file3"))
       action.log(message_type="Task 2 created", thread=task3.get_name()) """
    tic = time.perf_counter()
    with start_action(action_type="Creating threads and starting threadss")as action: 
        thread1 = Thread(target=preserve_context(GetIsoFile),kwargs={"filename":"iso1"})
        thread2 = Thread(target=preserve_context(GetIsoFile),kwargs={"filename":"iso2"})
        thread3 = Thread(target=preserve_context(GetIsoFile),kwargs={"filename":"iso3"})
        action.log(message_type="Thread ids:", thread1=thread1.name, thread2=thread2.name, thread3=thread3.name)
        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()
        toc = time.perf_counter()
    
    with start_action(action_type="Performance:") as action:
        action.log(message_type=f"Downloaded the files in {toc -tic:0.4f} seconds")


main()