"""
Solar energy estimation using NASA POWER API
"""
import urllib.request
import urllib.parse
import json
import functools
from config.settings import API_SETTINGS

class EnergyEstimator:
    def __init__(self):
        self.base_url = API_SETTINGS['nasa_power_base_url']
        self.timeout = API_SETTINGS['request_timeout']
        self.cache_size = API_SETTINGS['cache_size']
    
    @functools.lru_cache(maxsize=32)
    def _cached_nasa_call(self, lon, lat):
        """Cached NASA POWER API call to avoid repeated requests"""
        params = {
            "parameters": "ALLSKY_SFC_SW_DWN",
            "community": "RE",
            "longitude": f"{lon:.4f}",
            "latitude":  f"{lat:.4f}",
            "format": "JSON"
        }
        
        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(url, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode())
            
        value = data.get("properties", {}).get("parameter", {}).get("ALLSKY_SFC_SW_DWN", {}).get("ANN")
        
        if value is None or value < 0:
            raise ValueError("Invalid NASA POWER response")
            
        return value
    
    def fetch_solar_irradiance(self, lon, lat):
        """Fetch average daily solar irradiance from NASA POWER API"""
        try:
            # Round coordinates to reduce cache misses
            return self._cached_nasa_call(round(lon, 4), round(lat, 4))
        except Exception as e:
            raise Exception(f"NASA POWER API error: {e}")
    
    def calculate_energy_production(self, num_panels, panel_area_m2, panel_efficiency, performance_ratio, avg_daily_irradiance_kwh_m2):
        """
        Calculate solar energy production
        
        Args:
            num_panels: Number of solar panels
            panel_area_m2: Area of each panel in square meters
            panel_efficiency: Panel efficiency (0-1, e.g., 0.18 for 18%)
            performance_ratio: System performance ratio (0-1, typically 0.8)
            avg_daily_irradiance_kwh_m2: Average daily solar irradiance in kWh/m²/day
            
        Returns:
            dict: Energy production metrics
        """
        if num_panels == 0:
            return {
                'daily_energy_kwh': 0.0,
                'annual_energy_kwh': 0.0,
                'total_panel_area_m2': 0.0
            }
        
        # Calculate daily energy per panel
        energy_daily_per_panel_kwh = (
            avg_daily_irradiance_kwh_m2 * 
            panel_area_m2 * 
            panel_efficiency * 
            performance_ratio
        )
        
        # Calculate totals
        total_daily_energy_kwh = energy_daily_per_panel_kwh * num_panels
        total_annual_energy_kwh = total_daily_energy_kwh * 365
        total_panel_area_m2 = num_panels * panel_area_m2
        
        return {
            'daily_energy_kwh': total_daily_energy_kwh,
            'annual_energy_kwh': total_annual_energy_kwh,
            'total_panel_area_m2': total_panel_area_m2
        }
    
    def validate_energy_parameters(self, panel_efficiency, performance_ratio):
        """Validate energy calculation parameters"""
        errors = []
        
        try:
            efficiency = float(panel_efficiency)
            if not (0 < efficiency <= 100):
                errors.append("Panel efficiency must be between 0 and 100%")
        except ValueError:
            errors.append("Invalid panel efficiency value")
        
        try:
            perf_ratio = float(performance_ratio)
            if not (0 < perf_ratio <= 1):
                errors.append("Performance ratio must be between 0 and 1")
        except ValueError:
            errors.append("Invalid performance ratio value")
        
        return errors