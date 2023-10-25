import logging
import urllib.parse
from os import getenv
from time import sleep

import dotenv
import requests


class Plex:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        logging.INFO("Initializing Plex Library")
        self.url = getenv("PLEX_URL")
        self.apiKey = getenv("PLEX_API")

    def scan_mediaFolder(self, moviePath, LibraryID=1):
        encoded_path = urllib.parse.quote(moviePath, safe="")
        logging.INFO(f"Scanning {encoded_path}")
        url = f"{self.url}/library/sections/{LibraryID}/refresh?path={encoded_path}&X-Plex-Token={self.apiKey}"

        payload = {}
        headers = {}

        requests.request("GET", url, headers=headers, data=payload)
        sleep(2)


if __name__ == "__main__":
    log = "info"
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log)
    logging.basicConfig(filename="plex.log", encoding="utf-8", level=numeric_level)
    x = Plex()
    x.scan_mediaFolder(moviePath="/mnt/Storage/Media/Movies/Back to the Future (1985)")
