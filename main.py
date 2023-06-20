import plex
import radarr
import overseerr
import pprint
import os
import schedule
import time

def get_Media():

    movies = radarr.Radarr()
    requests = overseerr.Overseerr()

    total_Movies = movies.get_Movies()
    total_Requests = requests.get_Movies()

    for item in total_Requests:
        if item['externalServiceId'] in total_Movies:
            total_Movies[item['externalServiceId']]['OverseerrID'] = item['id']

    return total_Movies

def remove_Media():

    movies_parsed = get_Media()
    r = radarr.Radarr()
    o = overseerr.Overseerr()
    p = plex.Plex()
    pprint.pprint(movies_parsed)
    if len(movies_parsed) >= 1:
        for key in movies_parsed.keys():
            r.delete_Movie(key)
            print(f"Radarr: {movies_parsed[key]['title']}")
            o.delete_Movie(movies_parsed[key]['OverseerrID'])
            print(f"Overseer: {movies_parsed[key]['title']}")
            p.scan_mediaFolder(moviePath=movies_parsed[key]['path'])
            print(f"Plex: {movies_parsed[key]['title']}")
    else:
        print('Nothing to remove, skipping')
if __name__ == "__main__":

    env_File = ['RADARR_URL', 'RADARR_API', 'RADARR_TAG', 
                'PLEX_API', 'PLEX_URL', 'OVERSEERR_API', 
                'OVERSEER_URL', 'DAYS_TO_KEEP']
    if os.path.isfile('.env') is False:
        with open('.env', 'w') as f:
            for line in env_File:
                f.write(f'{line}=\n')
            f.close()
            print('.env file generated')
    else:
        remove_Media()
        schedule.every().day.at("01:00").do(remove_Media)

        while True:
            schedule.run_pending()
            time.sleep(1)