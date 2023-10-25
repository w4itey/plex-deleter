import json
import logging
import urllib.parse
import urllib.request
from os import getenv

import dotenv
import requests


class Overseerr:
    def __init__(self, log="debug") -> None:
        logging.info("Loading local env file")
        dotenv.load_dotenv()
        self.apiKey = getenv("OVERSEERR_API")
        self.url = getenv("OVERSEERR_URL")

    def get_Movies(self):
        url = f"{self.url}/api/v1/media?take=5000&filter=all&sort=added"

        payload = {}
        headers = {"Accept": "application/json", "X-Api-Key": self.apiKey}

        response = requests.request("GET", url, headers=headers, data=payload)
        results = response.json()["results"]
        return results

    def delete_Movie(self, id):
        url = f"{self.url}/api/v1/media/{id}"

        payload = {}
        headers = {"X-Api-Key": self.apiKey}
        logging.info(f"Preparing to delete {id} in Overseerr")
        response = requests.request("DELETE", url, headers=headers, data=payload)

        logging.info(response.text)

    def search(self, title):
        search = urllib.parse.quote_plus(title)

        url = f"{self.url}/api/v1/search?query={search}&page=1&language=en"

        payload = {}
        headers = {"X-Api-Key": self.apiKey}

        response = requests.request("GET", url, headers=headers, data=payload)
        logging.info(f"Searching for Movie {title}")

        if response.status_code == 200:
            logging.info(f"Movie found {title}")
            logging.debug(response.json())

        return response.json()

    def add_popular_movies(self):
        stenvenLU = "https://popular-movies-data.stevenlu.com/movies.json"
        data = requests.request("GET", stenvenLU)
        output = data.json()
        logging.info("Processing Stenven Lu Popular Movie List")
        logging.debug(output)

        url = f"{self.url}/api/v1/request"

        for item in output:
            # x = self.search(item["title"])

            payload = json.dumps(
                {
                    "mediaType": "movie",
                    "mediaId": item["tmdb_id"],
                    "is4k": False,
                    "userId": 7,
                }
            )

            headers = {
                "X-Api-Key": self.apiKey,
                "accept": "application/json",
                "Content-Type": "application/json",
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                logging.info(f'{item['title']}: Added to Overseer')
                logging.debug(item)
                logging.debug(response.json())
            elif response.status_code == 409:
                logging.info(f'{item['title']}: Already added to Overseer')
                logging.debug(item)
                logging.debug(response.json())


if __name__ == "__main__":
    log = "info"
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log)
    logging.basicConfig(filename="overseerr.log", encoding="utf-8", level=numeric_level)
    x = Overseerr()
    x.add_popular_movies()
