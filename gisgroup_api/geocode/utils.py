"""
    gisgroup_api.geocode.utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Provide geocoding capabilities
"""

import requests

def findone(query):
    payload = {
        'q': query,
        'per_side': 1,
    }

    response = requests.get("http://dawa.aws.dk/adresser", params=payload)
    json = response.json()

    return json[0]
