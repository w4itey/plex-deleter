import requests
import dotenv
from os import getenv
import urllib.parse
from time import sleep

class Plex():

    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.url = getenv("PLEX_URL")
        self.apiKey = getenv("PLEX_API")
        
    def scan_mediaFolder(self, moviePath, LibraryID=1):
        
        encoded_path = urllib.parse.quote(moviePath, safe='')
        url = f"{self.url}/library/sections/{LibraryID}/refresh?path={encoded_path}&X-Plex-Token={self.apiKey}"

        payload = {}
        headers = {
        }

        requests.request("GET", url, headers=headers, data=payload)
        sleep(2)

if __name__ == "__main__":

    x = Plex()
    x.scan_mediaFolder(moviePath="/mnt/Storage/Media/Movies/Back to the Future (1985)")