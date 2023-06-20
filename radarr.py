import requests
import datetime
import dotenv
from os import getenv
import pytz
import pprint
from time import sleep

class Radarr:

    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.apiKey = getenv("RADARR_API")
        self.url = getenv("RADARR_URL")
        self.KeepTime = int(getenv("DAYS_TO_KEEP"))
        self.tag = getenv("RADARR_TAG")
        self.tagID = False

    def get_Tag(self):

        url = f"{self.url}/api/v3/tag"

        payload = {}
        headers = {
        'X-Api-Key': self.apiKey
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        for item in response.json():
            if item['label'] == self.tag:
                self.tagID = item['id']

    def get_Movies(self):

        self.get_Tag()
        url = f"{self.url}/api/v3/movie"

        payload = {}
        headers = {
        'X-Api-Key': self.apiKey
        }

        movies = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        for entry in response:
            if entry["hasFile"] is True:
                if self.tagID in entry['tags']:
                    if datetime.datetime.fromisoformat(entry["movieFile"]["dateAdded"]) < datetime.datetime.now(pytz.timezone('America/New_York')) - datetime.timedelta(days=self.KeepTime):
                        dateAdded = datetime.datetime.fromisoformat(entry["movieFile"]["dateAdded"])
                        title = entry["title"]
                        path = entry['path']
                        id = entry['id']
                        movies[id] = {'title': title, 'path': path, 'dateadded': dateAdded}
        return movies
    
    def delete_Movie(self, id):
        
        url = f"{self.url}/api/v3/movie/{id}?deleteFiles=true&addImportExclusion=false"
        payload = {}
        headers = {
        'X-Api-Key': self.apiKey
        }

        requests.request("DELETE", url, headers=headers, data=payload)
        sleep(10)


if __name__ == "__main__":

    x = Radarr()
    pprint.pprint(x.get_Movies())