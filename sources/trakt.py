import pprint
from os import getenv

import dotenv
import requests


class Trakt:
    def __init__(self) -> None:
        self.clientID = (
            "9431b71ca35fabcad233de95f610ea3bc6c623af25522c1adf2bc653635b9091"
        )
        dotenv.load_dotenv()
        self.apiKey = getenv("TRAKT_ID")

    def get_popular(self):
        movie_List = {}
        trakt_items = [
            "https://api.trakt.tv/movies/popular",
            "https://api.trakt.tv/movies/trending",
        ]

        for trakt_url in trakt_items:
            url = f"{trakt_url}?&page=1&limit=30"
            headers = {
                "Content-Type": "application/json",
                "trakt-api-version": "2",
                "trakt-api-key": self.apiKey,
            }

            response = requests.request("GET", url, headers=headers)

            for item in response.json():
                if item.get("ids"):
                    movie_List[item["title"]] = {
                        "tmdb": item["ids"]["tmdb"],
                        "mediaType": "movie"
                        }
                elif item.get("movie"):
                    movie_List[item["movie"]["title"]] = {
                        "tmdb": item["movie"]["ids"]["tmdb"],
                        "mediaType": "movie"
                    }
        return movie_List


if __name__ == "__main__":
    x = Trakt()
    pprint.pprint(x.get_popular())
