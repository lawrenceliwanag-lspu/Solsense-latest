"""
Unit conversion and coordinate transformation utilities
"""
import rasterio.warp
import numpy as np

class ConversionUtils:
    def __init__(self):
        pass
    
    def convert_area_to_meters(self, width_input, height_input, unit):
        """
        Convert input dimensions to meters based on unit
        
        Args:
            width_input: Width or area value as string
            height_input: Height value as string (ignored for hectares)
            unit: "meters" or "hectares"
            
        Returns:
            tuple: (width_m, height_m) in meters
        """
        if unit == "hectares":
            # Width input contains the area in hectares
            area_hectares = float(width_input)
            area_m2 = area_hectares * 10000
            
            # Create a square area from the hectares
            side_length = area_m2 ** 0.5
            return side_length, side_length
            
        else:
            # Already in meters
            width = float(width_input)
            height = float(height_input)
            return width, height
    
    def convert_meters_to_display_unit(self, width_m, height_m, unit):
        """Convert meter dimensions back to display unit"""
        if unit == "hectares":
            area_m2 = width_m * height_m
            area_hectares = area_m2 / 10000
            return f"{area_hectares:.3f}", "N/A"
        else:
            return f"{width_m:.0f}", f"{height_m:.0f}"
    
    def calculate_land_area(self, width_input, height_input, unit):
        """Calculate land area in square meters"""
        try:
            if unit == "hectares":
                area_hectares = float(width_input)
                return area_hectares * 10000
            else:
                width = float(width_input)
                height = float(height_input)
                return width * height
        except ValueError:
            return 0.0
    
    def pixel_to_geographic(self, pixel_coords, transform, original_crs):
        """
        Convert pixel coordinates to geographic coordinates
        
        Args:
            pixel_coords: (col, row) pixel coordinates
            transform: Rasterio transform object
            original_crs: Original coordinate reference system
            
        Returns:
            tuple: (longitude, latitude) in WGS84
        """
        col, row = pixel_coords
        
        # Convert pixel to coordinate system units
        x_coord, y_coord = rasterio.transform.xy(transform, row, col, offset='center')
        
        # Convert to WGS84 if not already geographic
        if not original_crs.is_geographic:
            lons_lats = rasterio.warp.transform(
                original_crs, 
                {'init': 'epsg:4326'}, 
                [x_coord], 
                [y_coord]
            )
            lon, lat = lons_lats[0][0], lons_lats[1][0]
        else:
            lon, lat = x_coord, y_coord
            
        return lon, lat
    
    def format_coordinates(self, lon, lat, precision=4):
        """Format coordinates for display"""
        return f"{lon:.{precision}f}°", f"{lat:.{precision}f}°"
    
    def format_area(self, area_m2):
        """Format area for display with appropriate units"""
        if area_m2 >= 10000:
            hectares = area_m2 / 10000
            return f"{hectares:.2f} ha ({area_m2:,.0f} m²)"
        else:
            return f"{area_m2:,.0f} m²"
    
    def format_energy(self, energy_kwh):
        """Format energy values for display"""
        if energy_kwh >= 1000000:
            mwh = energy_kwh / 1000
            return f"{mwh:.1f} MWh"
        elif energy_kwh >= 1000:
            return f"{energy_kwh/1000:.1f} MWh"
        else:
            return f"{energy_kwh:,.0f} kWh"