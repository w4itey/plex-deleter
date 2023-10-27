import pprint

import requests


class StevenLu:
    def __init__(self) -> None:
        pass

    def get_popular(self):
        movie_List = {}
        stenvenLU = "https://popular-movies-data.stevenlu.com/movies.json"
        data = requests.request("GET", stenvenLU)
        output = data.json()

        for item in output:
            movie_List[item["title"]] = {
                "tmdb": item["tmdb_id"], 
                "mediaType": "movie"
                }
        return movie_List


if __name__ == "__main__":
    x = StevenLu()
    pprint.pprint(x.get_popular())
