import subprocess
import sys
import time
import requests

from os import listdir


DIR = "./scenes/"


def print_characters(TIME, output):
    for letter in output:
        print(letter, end="", flush=True)
        time.sleep(TIME)
    print()


def play_scenes(settings):
    while True:
        req = requests.get(IP+"/scene")
        print_characters(settings["character_time"], req.json()["text"])
        time.sleep(settings["pause_time"])


def main(IP):
    req = requests.get(IP+"/settings")
    play_scenes(req.json())


if __name__ == "__main__":
    IP = sys.argv[1]
    main(IP)
