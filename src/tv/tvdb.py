from datetime import datetime, date
import logging

import requests

from . import settings


logger = logging.getLogger(__name__)
TOKEN = None


def token():
    global TOKEN
    if TOKEN is None:
        logger.info("Authenticating with thetvdb api for JWT")
        response = requests.post("https://api.thetvdb.com/login", json={"apikey": settings.API_KEY})
        response.raise_for_status()
        TOKEN = response.json()['token']
    return TOKEN


def query_series(series_id):
    logger.info(f"{series_id}: Querying series data")
    response = requests.get(
        f"https://api.thetvdb.com/series/{series_id}",
        headers={'Authorization': f"Bearer {token()}"}
    )
    response.raise_for_status()
    series = response.json()['data']

    page = 1
    episodes = []
    while True:
        logger.info(f"{series_id}: Querying episode data (page {page})")
        response = requests.get(
            f"https://api.thetvdb.com/series/{series_id}/episodes",
            headers={'Authorization': f"Bearer {token()}"},
            params={"page": page}
        )
        response.raise_for_status()
        result = response.json()
        # Ignore specials with season 0
        episodes.extend([e for e in result['data'] if e['airedSeason'] != 0])
        if result['links']['last'] == page:
            break
        page += 1
    return series, episodes


def search(series_name):
    logger.info(f"Searching thetvdb for '{series_name}'")
    response = requests.get(
        f"https://api.thetvdb.com/search/series",
        headers={'Authorization': f"Bearer {token()}"},
        params={'name': series_name}
    )
    response.raise_for_status()
    return response.json()['data']
