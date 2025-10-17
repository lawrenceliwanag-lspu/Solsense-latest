"""
GeoTIFF file loading and basic processing
"""
import rasterio
import numpy as np
from rasterio.windows import Window
from rasterio.transform import Affine
from rasterio.crs import CRS

class GeoTIFFHandler:
    def __init__(self):
        pass
    
    def load_geotiff(self, filepath):
        """Load GeoTIFF file and extract basic information"""
        try:
            with rasterio.open(filepath) as src:
                # Read basic metadata
                original_crs = src.crs
                transform = src.transform
                dem_data = src.read(1).astype(np.float32)
                nodata_value = src.nodata
                
                # Handle nodata values
                if nodata_value is not None:
                    dem_data[dem_data == nodata_value] = np.nan
                
                # Calculate pixel dimensions
                pixel_width_m = abs(transform.a)
                pixel_height_m = abs(transform.e)
                
                return {
                    'dem_data': dem_data,
                    'original_crs': original_crs,
                    'transform': transform,
                    'nodata_value': nodata_value,
                    'pixel_width_m': pixel_width_m,
                    'pixel_height_m': pixel_height_m
                }
                
        except Exception as e:
            raise Exception(f"Error loading GeoTIFF: {e}")
    
    def validate_geotiff(self, filepath):
        """Validate GeoTIFF file before loading"""
        try:
            with rasterio.open(filepath) as src:
                if not src.crs:
                    return False, "GeoTIFF does not have a CRS defined"
                if not src.transform:
                    return False, "GeoTIFF does not have a geotransform"
                return True, "Valid GeoTIFF file"
        except Exception as e:
            return False, f"Invalid GeoTIFF file: {e}"