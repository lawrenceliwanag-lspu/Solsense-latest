"""
Centralized data state management
"""
import numpy as np

class DataManager:
    def __init__(self):
        # File and GeoTIFF data
        self.filepath = None
        self.dataset = None
        self.slope_degrees = None
        self.aspect_degrees = None
        self.original_crs = None
        self.transform = None
        self.display_image_rgba = None
        self.nodata_value = None
        self.pixel_width_m = 1.0
        self.pixel_height_m = 1.0
        
        # Marker and location data
        self.marker_pixel_coords = None
        self.marker_lon_lat = None
        self.location_name = "Not Set"
        
        # Analysis results
        self.num_panels_packed = 0
        self.annual_energy_kwh = 0.0
        self.daily_energy_kwh = 0.0
        self.land_area_m2 = 0.0
        
        # Visualization objects (managed by UI)
        self.marker_object = None
        self.land_area_rect_patch = None
        self.packed_object_patches = []
    
    def clear_data(self):
        """Reset all data to initial state"""
        self.filepath = None
        self.dataset = None
        self.slope_degrees = None
        self.aspect_degrees = None
        self.original_crs = None
        self.transform = None
        self.display_image_rgba = None
        self.nodata_value = None
        self.pixel_width_m = 1.0
        self.pixel_height_m = 1.0
        
    def clear_marker(self):
        """Clear marker-related data"""
        self.marker_pixel_coords = None
        self.marker_lon_lat = None
        self.location_name = "Not Set"
        
    def clear_analysis_results(self):
        """Clear analysis results"""
        self.num_panels_packed = 0
        self.annual_energy_kwh = 0.0
        self.daily_energy_kwh = 0.0
        self.land_area_m2 = 0.0
        
    def get_marker_slope_aspect(self):
        """Get slope and aspect values at marker location"""
        if not self.marker_pixel_coords or self.slope_degrees is None:
            return None, None
            
        col, row = self.marker_pixel_coords
        if (0 <= row < self.slope_degrees.shape[0] and 
            0 <= col < self.slope_degrees.shape[1]):
            slope_val = self.slope_degrees[row, col]
            aspect_val = self.aspect_degrees[row, col]
            return slope_val, aspect_val
        return None, None
    
    def is_data_loaded(self):
        """Check if GeoTIFF data is loaded"""
        return self.slope_degrees is not None
    
    def is_marker_set(self):
        """Check if marker is set"""
        return self.marker_pixel_coords is not None