from geopy.geocoders import Nominatim
import geopandas as gpd

def city_from_coord(latitude, longitude):
    geolocator = Nominatim(user_agent="reverse_geocoding_example")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        address = location.raw.get('address', {})
        city = address.get('city', 'N/A')
        state = address.get('state', 'N/A')
        return city, state
    else:
        return 'N/A', 'N/A'
