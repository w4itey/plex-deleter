import datetime
import logging
import pprint
from os import getenv
from time import sleep

import dotenv
import pytz
import requests


class Radarr:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        logging.INFO("Initializing Radarr Library")
        self.apiKey = getenv("RADARR_API")
        self.url = getenv("RADARR_URL")
        self.KeepTime = int(getenv("DAYS_TO_KEEP"))
        self.tag = getenv("RADARR_TAG")
        self.tagID = False

    def get_Tag(self):
        url = f"{self.url}/api/v3/tag"

        payload = {}
        headers = {"X-Api-Key": self.apiKey}

        response = requests.request("GET", url, headers=headers, data=payload)

        logging.INFO("Getting Tag ID")
        for item in response.json():
            if item["label"] == self.tag:
                self.tagID = item["id"]
                logging.INFO(f"Found tag ID {self.tagID}")

    def get_Movies(self):
        self.get_Tag()
        url = f"{self.url}/api/v3/movie"

        payload = {}
        headers = {"X-Api-Key": self.apiKey}

        movies = {}
        logging.INFO("Looking for Movies")
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        for entry in response:
            if entry["hasFile"] is True:
                if self.tagID in entry["tags"]:
                    if datetime.datetime.fromisoformat(
                        entry["movieFile"]["dateAdded"]
                    ) < datetime.datetime.now(
                        pytz.timezone("America/New_York")
                    ) - datetime.timedelta(days=self.KeepTime):
                        dateAdded = datetime.datetime.fromisoformat(
                            entry["movieFile"]["dateAdded"]
                        )
                        title = entry["title"]
                        path = entry["path"]
                        id = entry["id"]
                        movies[id] = {
                            "title": title,
                            "path": path,
                            "dateadded": dateAdded,
                        }
        logging.INFO(f"Found {movies}")
        return movies

    def delete_Movie(self, id):
        logging.INFO(f"Deleting movie ID: {id} in Radarr")
        url = f"{self.url}/api/v3/movie/{id}?deleteFiles=true&addImportExclusion=false"
        payload = {}
        headers = {"X-Api-Key": self.apiKey}

        requests.request("DELETE", url, headers=headers, data=payload)
        sleep(10)


if __name__ == "__main__":
    log = "info"
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log)
    logging.basicConfig(filename="radarr.log", encoding="utf-8", level=numeric_level)
    x = Radarr()
    pprint.pprint(x.get_Movies())
