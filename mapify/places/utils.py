import requests
from django.conf import settings

def search_places(query):
    """
    Interact with the Google Places API to search for places.
    """
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": settings.GOOGLE_PLACES_API_KEY,
    }
    response = requests.get(base_url, params=params)

    # Log the raw response data for debugging
    print(response.json())  # Debugging line

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from Google Places API"}
