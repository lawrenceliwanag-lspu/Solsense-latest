"""
Solar panel packing algorithms with performance monitoring
"""
from config.settings import APP_SETTINGS
import psutil
import time

class PackingSolver:
    def __init__(self):
        self.max_iterations = APP_SETTINGS['max_packing_iterations']
        self.last_execution_time = None
        self.last_memory_usage = None
    
    def next_fit_shelf_packing(self, land_width_m, land_height_m, obj_width_m, obj_height_m, num_objects_to_pack=None):
        """
        Pack rectangular objects (solar panels) using next-fit shelf algorithm
        
        Args:
            land_width_m: Available land width in meters
            land_height_m: Available land height in meters  
            obj_width_m: Object width in meters
            obj_height_m: Object height in meters
            num_objects_to_pack: Max number of objects to pack (None = fill maximum)
            
        Returns:
            list: List of packed object coordinates with x, y, w, h
        """
        # Get process for memory monitoring
        process = psutil.Process()
        
        # Record initial memory usage (in MB)
        mem_before = process.memory_info().rss / 1024 / 1024
        
        # Start timing
        start_time = time.time()
        
        horizontal_gap_m = 0.02
        row_gap_m = 1.5
        obj_width_m = obj_width_m + horizontal_gap_m
        obj_height_m = obj_height_m + row_gap_m
        packed_objects_coords = []
        current_x_m = 0.0
        shelf_bottom_y_m = 0.0
        shelf_effective_height_m = obj_height_m
        objects_placed = 0

        # Validate inputs
        if obj_width_m <= 0 or obj_height_m <= 0:
            return []
        if obj_width_m > land_width_m or obj_height_m > land_height_m:
            return []

        iter_count = 0

        while iter_count < self.max_iterations:
            iter_count += 1
            
            # Check if we've reached the specified number
            if num_objects_to_pack is not None and objects_placed >= num_objects_to_pack:
                break

            # Check if current shelf can fit another object vertically
            if shelf_bottom_y_m + shelf_effective_height_m <= land_height_m:
                # Try to place object horizontally on current shelf
                if current_x_m + obj_width_m <= land_width_m:
                    # Object fits, place it
                    packed_objects_coords.append({
                        'x': current_x_m, 
                        'y': shelf_bottom_y_m, 
                        'w': obj_width_m, 
                        'h': obj_height_m
                    })
                    current_x_m += obj_width_m
                    objects_placed += 1
                    continue
                else:
                    # Move to next shelf
                    current_x_m = 0.0
                    shelf_bottom_y_m += shelf_effective_height_m
                    
                    # Check if new shelf can fit vertically and place first object
                    if shelf_bottom_y_m + shelf_effective_height_m <= land_height_m:
                        if current_x_m + obj_width_m <= land_width_m:
                            packed_objects_coords.append({
                                'x': current_x_m, 
                                'y': shelf_bottom_y_m, 
                                'w': obj_width_m, 
                                'h': obj_height_m
                            })
                            current_x_m += obj_width_m
                            objects_placed += 1
                            continue
                        else:
                            break  # Can't fit even one object on new shelf
                    else:
                        break  # No more vertical space
            else:
                break  # No more vertical space

        if iter_count >= self.max_iterations:
            print(f"Warning: Packing reached max iterations ({self.max_iterations}).")
        
        # End timing
        end_time = time.time()
        
        # Record final memory usage (in MB)
        mem_after = process.memory_info().rss / 1024 / 1024
        
        # Calculate metrics
        self.last_execution_time = end_time - start_time
        self.last_memory_usage = mem_after - mem_before
        
        # Print performance metrics
        print(f"Performance Metrics for next_fit_shelf_packing:")
        print(f"  Execution Time: {self.last_execution_time:.6f} seconds")
        print(f"  Memory Usage: {self.last_memory_usage:.4f} MB")
        print(f"  Objects Packed: {objects_placed}")
        print(f"  Iterations: {iter_count}")
    
        return packed_objects_coords
    
    def get_performance_stats(self):
        """Return the last recorded performance statistics"""
        return {
            'execution_time_seconds': self.last_execution_time,
            'memory_usage_mb': self.last_memory_usage
        }
    
    def calculate_packing_efficiency(self, packed_objects, land_width_m, land_height_m, obj_width_m, obj_height_m):
        """Calculate packing efficiency metrics"""
        total_land_area = land_width_m * land_height_m
        total_object_area = len(packed_objects) * obj_width_m * obj_height_m
        efficiency = (total_object_area / total_land_area) * 100 if total_land_area > 0 else 0
        
        return {
            'num_objects': len(packed_objects),
            'total_land_area_m2': total_land_area,
            'total_object_area_m2': total_object_area,
            'efficiency_percent': efficiency
        }