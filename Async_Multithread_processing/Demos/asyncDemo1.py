import asyncio
from threading import Thread
import time
from tracemalloc import start
import requests
from pathlib import Path
from eliot import start_action, to_file
to_file(open("D:\Repositories\Work-Experiments\Logs\outputAsync.log", "w"))

DOWNLOAD_FOLDER =Path("D:\\Repositories\\Work-Experiments\\Downlaods")
ISO_FILE="https://cdimage.debian.org/cdimage/archive/9.13.0/amd64/iso-cd/debian-9.13.0-amd64-netinst.iso"
async def GetIsoFile(filename: str):
    with start_action(action_type=f"Getting {filename}: Started at {time.strftime('%X')}", thread=Thread.__name__) as action:
        resp = requests.api.get(ISO_FILE)
        if resp.status_code == 200:
            open((DOWNLOAD_FOLDER/filename).with_suffix(".iso"), "wb").write(resp.content)
        action.log(message_type=f"Completed getting {filename} at {time.strftime('%X')}", thread=Thread.__name__)
        await asyncio.sleep(1)


async def main():
    """ task = []
    with start_action(action_type="creating tasks:") as action:
       task1 = asyncio.create_task()
       action.log(message_type="Task 1 created", thread=task1.get_name())
       task2 = asyncio.create_task(GetIsoFile("file2"))
       action.log(message_type="Task 2 created", thread=task2.get_name())
       task3  = asyncio.create_task(GetIsoFile("file3"))
       action.log(message_type="Task 2 created", thread=task3.get_name()) """
    tic = time.perf_counter()
    with start_action(action_type="gathering list of tasks")as action: 
        await asyncio.gather(GetIsoFile("file1"), GetIsoFile("file2"), GetIsoFile("file3"))
        toc = time.perf_counter()
    
    with start_action(action_type="Performance:") as action:
        action.log(message_type=f"Downloaded the file in {toc -tic:0.4f} seconds")



asyncio.run(main())    