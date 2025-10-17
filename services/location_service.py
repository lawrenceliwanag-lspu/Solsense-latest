"""
Location services for geocoding and reverse geocoding
"""
import requests
from config.settings import API_SETTINGS

class LocationService:
    def __init__(self):
        self.nominatim_base_url = API_SETTINGS['nominatim_base_url']
        self.timeout = API_SETTINGS['request_timeout']
    
    def reverse_geocode(self, lon, lat):
        """
        Get location name from coordinates using Nominatim API
        
        Args:
            lon: Longitude
            lat: Latitude
            
        Returns:
            str: Formatted location name
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'addressdetails': 1
            }
            headers = {
                'User-Agent': 'SolSense-GeoTIFF-Viewer/1.0'
            }
            
            response = requests.get(
                self.nominatim_base_url, 
                params=params, 
                headers=headers, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._format_location_name(data)
            else:
                return 'Location Unavailable'
                
        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return 'Location Error'
    
    def _format_location_name(self, nominatim_data):
        """Format location name from Nominatim response"""
        address = nominatim_data.get('address', {})
        name_parts = []

        # Try to get street information first
        street_info = []
        if 'house_number' in address:
            street_info.append(address['house_number'])
        if 'road' in address:
            street_info.append(address['road'])
        elif 'street' in address:
            street_info.append(address['street'])

        if street_info:
            name_parts.append(' '.join(street_info))

        # Add neighborhood/suburb if available
        for key in ['neighbourhood', 'suburb', 'quarter', 'district']:
            if key in address:
                name_parts.append(address[key])
                break

        # Try to get city/town/village
        for key in ['city', 'town', 'village', 'municipality']:
            if key in address:
                name_parts.append(address[key])
                break

        # Add state/province (shortened for space)
        for key in ['state', 'province', 'region']:
            if key in address:
                name_parts.append(address[key])
                break

        if name_parts:
            return ', '.join(name_parts)
        else:
            # Fallback to display_name but truncate if too long
            display_name = nominatim_data.get('display_name', 'Unknown Location')
            return display_name[:50] + '...' if len(display_name) > 50 else display_name