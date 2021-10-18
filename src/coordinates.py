import requests
import json

def getCoordinates(hotel):
  # https://nominatim.openstreetmap.org/search?q=<query>&format=geojson
  # features -> 0 -> geometry -> coordinates

  try:
    r = requests.get(f'https://nominatim.openstreetmap.org/search?q={"+".join(hotel["address"].split(" "))}&format=geojson').content
    coords = json.loads(r)['features'][0]['geometry']['coordinates']
    hotel['coordinates'] = {'latitude': coords[1], 'longitude': coords[0]}
  except (IndexError, json.JSONDecodeError):
    hotel['coordinates'] = None
