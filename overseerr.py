import requests
import dotenv
from os import getenv
import pprint

class Overseerr:

    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.apiKey = getenv('OVERSEERR_API')
        self.url = getenv('OVERSEERR_URL')

    def get_Movies(self):

        url = f"{self.url}/api/v1/media?take=5000&filter=all&sort=added"

        payload = {}
        headers = {
        'Accept': 'application/json',
        'X-Api-Key': self.apiKey
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        results = response.json()['results']
        return results
    
    def delete_Movie(self, id):

        url = f"{self.url}/api/v1/media/{id}"

        payload = {}
        headers = {
        'X-Api-Key': self.apiKey
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text)



if __name__ == "__main__":
    x = Overseerr()
    x.delete_Movie(487)