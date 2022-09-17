import time
import random
import threading
import requests

endpoints = ("", "files", "upload", "create", "delete")
HOST = "http://127.0.0.1:5000/"


def run():
    while True:
        try:
            target = random.choice(endpoints)
            requests.get(HOST+target)
        except requests.RequestException:
            print("cannot connect", HOST)
            time.sleep(1)

if __name__ == "__main__":
    for _ in range(4):
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    while True:
        time.sleep(1)
