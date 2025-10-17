"""
Slope and aspect calculations using Horn's method with performance monitoring
"""
import numpy as np
import psutil
import time

class SlopeCalculator:
    def __init__(self):
        self.last_execution_time = None
        self.last_memory_usage = None
    
    def calculate_slope_aspect_horn(self, dem, pixel_width, pixel_height):
        """
        Calculate slope and aspect using Horn's method
        
        Args:
            dem: Digital elevation model as numpy array
            pixel_width: Pixel width in meters
            pixel_height: Pixel height in meters
            
        Returns:
            tuple: (slope_degrees, aspect_degrees)
        """
        # Get process for memory monitoring
        process = psutil.Process()
        
        # Record initial memory usage (in MB)
        mem_before = process.memory_info().rss / 1024 / 1024
        
        # Start timing
        start_time = time.time()
        
        # Pad the DEM with edge values to handle borders
        padded_dem = np.pad(dem, pad_width=1, mode='edge')

        # Calculate gradients using Horn's method
        dz_dx = (
            (padded_dem[0:-2, 2:] + 2 * padded_dem[1:-1, 2:] + padded_dem[2:, 2:]) -
            (padded_dem[0:-2, 0:-2] + 2 * padded_dem[1:-1, 0:-2] + padded_dem[2:, 0:-2])
        ) / (8 * 30)  # 30m is typical pixel size, could be parameterized

        dz_dy = (
            (padded_dem[2:, 0:-2] + 2 * padded_dem[2:, 1:-1] + padded_dem[2:, 2:]) -
            (padded_dem[0:-2, 0:-2] + 2 * padded_dem[0:-2, 1:-1] + padded_dem[0:-2, 2:])
        ) / (8 * 30)

        # Calculate slope in radians then convert to degrees
        slope_rad = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
        slope_deg = np.degrees(slope_rad)

        # Calculate aspect (0 degrees is North)
        aspect_rad = np.arctan2(dz_dx, dz_dy)
        aspect_deg = np.degrees(aspect_rad)

        # Normalize aspect to 0-360 degrees
        aspect_deg[aspect_deg < 0] += 360

        # Set aspect to -1 for flat areas (very low slope)
        aspect_deg[slope_deg < 1e-6] = -1

        # Handle NaN values from original DEM
        nan_mask = np.isnan(dem)
        slope_deg[nan_mask] = np.nan
        aspect_deg[nan_mask] = np.nan
        
        # End timing
        end_time = time.time()
        
        # Record final memory usage (in MB)
        mem_after = process.memory_info().rss / 1024 / 1024
        
        # Calculate metrics
        self.last_execution_time = end_time - start_time
        self.last_memory_usage = mem_after - mem_before
        
        # Print performance metrics
        print(f"Performance Metrics for calculate_slope_aspect_horn:")
        print(f"  Execution Time: {self.last_execution_time:.6f} seconds")
        print(f"  Memory Usage: {self.last_memory_usage:.2f} MB")
        print(f"  Input DEM shape: {dem.shape}")

        return slope_deg, aspect_deg
    
    def get_performance_stats(self):
        """Return the last recorded performance statistics"""
        return {
            'execution_time_seconds': self.last_execution_time,
            'memory_usage_mb': self.last_memory_usage
        }
    
    def get_aspect_direction(self, degrees):
        """Convert aspect degrees to compass direction string"""
        if degrees < 0:
            return "Flat"
        if (degrees >= 337.5) or (degrees < 22.5):
            return "N"
        if (degrees >= 22.5) and (degrees < 67.5):
            return "NE"
        if (degrees >= 67.5) and (degrees < 112.5):
            return "E"
        if (degrees >= 112.5) and (degrees < 157.5):
            return "SE"
        if (degrees >= 157.5) and (degrees < 202.5):
            return "S"
        if (degrees >= 202.5) and (degrees < 247.5):
            return "SW"
        if (degrees >= 247.5) and (degrees < 292.5):
            return "W"
        if (degrees >= 292.5) and (degrees < 337.5):
            return "NW"
        return "N/A"
    
    def create_slope_visualization(self, slope_degrees, aspect_degrees, nodata_value=None):
        """Create RGBA visualization of slope data with suitability coloring"""
        slope_display = np.copy(slope_degrees)
        
        # Handle nodata values
        if nodata_value is not None:
            slope_display[np.isnan(slope_degrees)] = -9999
            
        valid_slope = slope_display[slope_display != -9999]
        if valid_slope.size == 0:
            return None
            
        # Normalize slope for grayscale base
        normalized_slope = (slope_display - np.nanmin(valid_slope)) / (np.nanmax(valid_slope) - np.nanmin(valid_slope))
        normalized_slope = np.nan_to_num(normalized_slope, nan=0)
        img_gray = (normalized_slope * 255).astype(np.uint8)
        
        # Create RGBA image
        display_image_rgba = np.zeros((slope_degrees.shape[0], slope_degrees.shape[1], 4), dtype=np.uint8)
        display_image_rgba[..., 0:3] = img_gray[..., np.newaxis]
        display_image_rgba[..., 3] = 255
        
        # Apply color coding for suitability
        low_slope_mask = (slope_degrees < 5) & (~np.isnan(slope_degrees))
        
        # South-facing slopes (SE, S, SW: 112.5° to 247.5°)
        south_facing_mask = (
            (aspect_degrees >= 112.5) & (aspect_degrees <= 247.5) & 
            (~np.isnan(aspect_degrees))
        )

        # Green tint for optimal areas (low slope AND south-facing)
        optimal_mask = low_slope_mask & south_facing_mask
        display_image_rgba[optimal_mask, 0] = np.clip(img_gray[optimal_mask] * 0.3, 0, 255)      # Less red
        display_image_rgba[optimal_mask, 1] = np.clip(img_gray[optimal_mask] * 0.7 + 100, 0, 255)  # More green
        display_image_rgba[optimal_mask, 2] = np.clip(img_gray[optimal_mask] * 0.3, 0, 255)      # Less blue

        # Yellow tint for suboptimal areas (low slope but not south-facing)
        suboptimal_mask = low_slope_mask & (~south_facing_mask)
        display_image_rgba[suboptimal_mask, 0] = np.clip(img_gray[suboptimal_mask] * 0.9 + 100, 0, 255)  # More red
        display_image_rgba[suboptimal_mask, 1] = np.clip(img_gray[suboptimal_mask] * 0.8 + 100, 0, 255)  # More green
        display_image_rgba[suboptimal_mask, 2] = np.clip(img_gray[suboptimal_mask] * 0.3, 0, 255)       # Less blue
        
        # Handle transparent areas for NaN
        nan_mask = np.isnan(slope_degrees)
        display_image_rgba[nan_mask, 3] = 0
        
        return display_image_rgba