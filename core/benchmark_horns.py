"""
Benchmark script for SlopeCalculator performance testing
"""
import time
import sys
import numpy as np
import argparse
import tracemalloc
import psutil
from pathlib import Path
from slope_calculator import SlopeCalculator

try:
    from osgeo import gdal
    GDAL_AVAILABLE = True
except ImportError:
    GDAL_AVAILABLE = False
    print("WARNING: GDAL not available. Install with: pip install GDAL")

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)  # Convert to MB

def load_geotiff(filepath):
    """Load a GeoTIFF file and extract DEM data and metadata"""
    if not GDAL_AVAILABLE:
        raise ImportError("GDAL is required to read GeoTIFF files")
    
    print(f"\nLoading GeoTIFF: {filepath}")
    dataset = gdal.Open(str(filepath), gdal.GA_ReadOnly)
    
    if dataset is None:
        raise ValueError(f"Could not open file: {filepath}")
    
    # Get raster band (assuming single band DEM)
    band = dataset.GetRasterBand(1)
    dem = band.ReadAsArray()
    
    # Get geotransform for pixel size
    geotransform = dataset.GetGeoTransform()
    pixel_width = abs(geotransform[1])  # pixel width in map units
    pixel_height = abs(geotransform[5])  # pixel height in map units
    
    # Get nodata value
    nodata = band.GetNoDataValue()
    
    # Replace nodata with NaN
    if nodata is not None:
        dem = dem.astype(float)
        dem[dem == nodata] = np.nan
    
    print(f"  Shape: {dem.shape}")
    print(f"  Pixel size: {pixel_width}m × {pixel_height}m")
    print(f"  Elevation range: {np.nanmin(dem):.2f}m to {np.nanmax(dem):.2f}m")
    print(f"  NoData value: {nodata}")
    
    dataset = None  # Close dataset
    
    return dem, pixel_width, pixel_height

def generate_test_dem(rows, cols, noise_level=10):
    """Generate synthetic DEM data for testing"""
    # Create a gradient with some random noise
    x = np.linspace(0, 100, cols)
    y = np.linspace(0, 100, rows)
    X, Y = np.meshgrid(x, y)
    
    # Base elevation with gradient
    dem = 100 + 0.5 * X + 0.3 * Y
    
    # Add some random terrain features
    dem += noise_level * np.random.randn(rows, cols)
    
    return dem

def benchmark_slope_calculator(geotiff_path=None):
    """Run performance tests on SlopeCalculator methods"""
    
    print("=" * 60)
    print("SLOPE CALCULATOR BENCHMARK")
    print("=" * 60)
    
    # Start memory tracking
    tracemalloc.start()
    initial_memory = get_memory_usage()
    print(f"\nInitial memory usage: {initial_memory:.2f} MB")
    
    calculator = SlopeCalculator()
    results = []
    
    # If GeoTIFF provided, test with real data
    if geotiff_path:
        if not GDAL_AVAILABLE:
            print("\nERROR: GDAL not available. Cannot load GeoTIFF.")
            print("Install with: pip install GDAL")
            return []
        
        try:
            dem_real, pixel_width, pixel_height = load_geotiff(geotiff_path)
            
            print("\n" + "=" * 60)
            print("REAL GEOTIFF DATA TEST")
            print("=" * 60)
            
            # Test with real GeoTIFF
            print(f"\nProcessing GeoTIFF ({dem_real.shape[0]}x{dem_real.shape[1]} pixels)")
            
            mem_before = get_memory_usage()
            tracemalloc.reset_peak()
            start_time = time.perf_counter()
            
            slope_real, aspect_real = calculator.calculate_slope_aspect_horn(
                dem=dem_real,
                pixel_width=pixel_width,
                pixel_height=pixel_height
            )
            
            end_time = time.perf_counter()
            mem_after = get_memory_usage()
            current, peak = tracemalloc.get_traced_memory()
            
            elapsed_real = end_time - start_time
            mem_used = mem_after - mem_before
            results.append(("Real GeoTIFF", elapsed_real, mem_used, peak / (1024 * 1024)))
            
            print(f"  DEM size: {dem_real.shape}")
            print(f"  Pixel size: {pixel_width}m × {pixel_height}m")
            print(f"  Time: {elapsed_real:.6f} seconds")
            print(f"  Memory used: {mem_used:.2f} MB (Peak: {peak / (1024 * 1024):.2f} MB)")
            print(f"  Avg slope: {np.nanmean(slope_real):.2f}°")
            print(f"  Max slope: {np.nanmax(slope_real):.2f}°")
            print(f"  Min slope: {np.nanmin(slope_real):.2f}°")
            
            # Aspect direction conversion for real data
            print(f"\nAspect direction conversion (real data)")
            valid_aspects = aspect_real[~np.isnan(aspect_real)]
            
            mem_before = get_memory_usage()
            tracemalloc.reset_peak()
            start_time = time.perf_counter()
            
            directions = [calculator.get_aspect_direction(a) for a in valid_aspects[:10000]]
            
            end_time = time.perf_counter()
            mem_after = get_memory_usage()
            current, peak = tracemalloc.get_traced_memory()
            
            elapsed_direction = end_time - start_time
            mem_used = mem_after - mem_before
            results.append(("Direction Conversion", elapsed_direction, mem_used, peak / (1024 * 1024)))
            
            print(f"  Samples processed: {len(directions)}")
            print(f"  Time: {elapsed_direction:.6f} seconds")
            print(f"  Memory used: {mem_used:.2f} MB (Peak: {peak / (1024 * 1024):.2f} MB)")
            
            # Visualization creation for real data
            print(f"\nSlope visualization (real data)")
            
            mem_before = get_memory_usage()
            tracemalloc.reset_peak()
            start_time = time.perf_counter()
            
            viz_real = calculator.create_slope_visualization(
                slope_degrees=slope_real,
                aspect_degrees=aspect_real
            )
            
            end_time = time.perf_counter()
            mem_after = get_memory_usage()
            current, peak = tracemalloc.get_traced_memory()
            
            elapsed_viz = end_time - start_time
            mem_used = mem_after - mem_before
            results.append(("Visualization", elapsed_viz, mem_used, peak / (1024 * 1024)))
            
            print(f"  Output shape: {viz_real.shape}")
            print(f"  Time: {elapsed_viz:.6f} seconds")
            print(f"  Memory used: {mem_used:.2f} MB (Peak: {peak / (1024 * 1024):.2f} MB)")
            
        except Exception as e:
            print(f"\nERROR loading GeoTIFF: {e}")
            print("Falling back to synthetic data tests...")
    
    # Synthetic data tests
    print("\n" + "=" * 60)
    print("SYNTHETIC DATA TESTS")
    print("=" * 60)
    
    # Test Case 1: Small DEM (100x100)
    print("\nTest 1: Small DEM (100x100 pixels)")
    
    mem_before = get_memory_usage()
    tracemalloc.reset_peak()
    start_time = time.perf_counter()
    
    dem_small = generate_test_dem(100, 100)
    slope_small, aspect_small = calculator.calculate_slope_aspect_horn(
        dem=dem_small,
        pixel_width=30,
        pixel_height=30
    )
    
    end_time = time.perf_counter()
    mem_after = get_memory_usage()
    current, peak = tracemalloc.get_traced_memory()
    
    elapsed_small = end_time - start_time
    mem_used = mem_after - mem_before
    results.append(("Small DEM", elapsed_small, mem_used, peak / (1024 * 1024)))
    
    print(f"  DEM size: {dem_small.shape}")
    print(f"  Time: {elapsed_small:.6f} seconds")
    print(f"  Memory used: {mem_used:.2f} MB (Peak: {peak / (1024 * 1024):.2f} MB)")
    print(f"  Avg slope: {np.nanmean(slope_small):.2f}°")
    
    # Test Case 2: Medium DEM (500x500)
    print("\nTest 2: Medium DEM (500x500 pixels)")
    
    mem_before = get_memory_usage()
    tracemalloc.reset_peak()
    start_time = time.perf_counter()
    
    dem_medium = generate_test_dem(500, 500)
    slope_medium, aspect_medium = calculator.calculate_slope_aspect_horn(
        dem=dem_medium,
        pixel_width=30,
        pixel_height=30
    )
    
    end_time = time.perf_counter()
    mem_after = get_memory_usage()
    current, peak = tracemalloc.get_traced_memory()
    
    elapsed_medium = end_time - start_time
    mem_used = mem_after - mem_before
    results.append(("Medium DEM", elapsed_medium, mem_used, peak / (1024 * 1024)))
    
    print(f"  DEM size: {dem_medium.shape}")
    print(f"  Time: {elapsed_medium:.6f} seconds")
    print(f"  Memory used: {mem_used:.2f} MB (Peak: {peak / (1024 * 1024):.2f} MB)")
    print(f"  Avg slope: {np.nanmean(slope_medium):.2f}°")
    
    # Test Case 3: Large DEM (1000x1000)
    print("\nTest 3: Large DEM (1000x1000 pixels)")
    
    mem_before = get_memory_usage()
    tracemalloc.reset_peak()
    start_time = time.perf_counter()
    
    dem_large = generate_test_dem(1000, 1000)
    slope_large, aspect_large = calculator.calculate_slope_aspect_horn(
        dem=dem_large,
        pixel_width=30,
        pixel_height=30
    )
    
    end_time = time.perf_counter()
    mem_after = get_memory_usage()
    current, peak = tracemalloc.get_traced_memory()
    
    elapsed_large = end_time - start_time
    mem_used = mem_after - mem_before
    results.append(("Large DEM", elapsed_large, mem_used, peak / (1024 * 1024)))
    
    print(f"  DEM size: {dem_large.shape}")
    print(f"  Time: {elapsed_large:.6f} seconds")
    print(f"  Memory used: {mem_used:.2f} MB (Peak: {peak / (1024 * 1024):.2f} MB)")
    print(f"  Avg slope: {np.nanmean(slope_large):.2f}°")
    
    # Test Case 4: Very Large DEM (2000x2000)
    print("\nTest 4: Very Large DEM (2000x2000 pixels)")
    
    mem_before = get_memory_usage()
    tracemalloc.reset_peak()
    start_time = time.perf_counter()
    
    dem_xlarge = generate_test_dem(2000, 2000)
    slope_xlarge, aspect_xlarge = calculator.calculate_slope_aspect_horn(
        dem=dem_xlarge,
        pixel_width=30,
        pixel_height=30
    )
    
    end_time = time.perf_counter()
    mem_after = get_memory_usage()
    current, peak = tracemalloc.get_traced_memory()
    
    elapsed_xlarge = end_time - start_time
    mem_used = mem_after - mem_before
    results.append(("Very Large DEM", elapsed_xlarge, mem_used, peak / (1024 * 1024)))
    
    print(f"  DEM size: {dem_xlarge.shape}")
    print(f"  Time: {elapsed_xlarge:.6f} seconds")
    print(f"  Memory used: {mem_used:.2f} MB (Peak: {peak / (1024 * 1024):.2f} MB)")
    print(f"  Avg slope: {np.nanmean(slope_xlarge):.2f}°")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_time = sum(r[1] for r in results)
    total_mem = sum(r[2] for r in results)
    max_peak_mem = max(r[3] for r in results)
    
    final_memory = get_memory_usage()
    memory_increase = final_memory - initial_memory
    
    for test_name, elapsed, mem_used, peak_mem in results:
        print(f"{test_name:25s}: {elapsed:.6f}s | Mem: {mem_used:+.2f} MB (Peak: {peak_mem:.2f} MB)")
    
    print(f"{'TOTAL TIME':25s}: {total_time:.6f} seconds")
    print(f"{'TOTAL MEM CHANGE':25s}: {total_mem:+.2f} MB")
    print(f"{'MAX PEAK MEMORY':25s}: {max_peak_mem:.2f} MB")
    print(f"{'FINAL MEMORY':25s}: {final_memory:.2f} MB (Change: {memory_increase:+.2f} MB)")
    print("=" * 60)
    
    # Stop memory tracking
    tracemalloc.stop()
    
    return results

def main():
    parser = argparse.ArgumentParser(
        description='Benchmark SlopeCalculator with optional GeoTIFF input',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with synthetic data only
  python benchmark_slope.py
  
  # Run with a real GeoTIFF file
  python benchmark_slope.py -g /path/to/dem.tif
  python benchmark_slope.py --geotiff elevation_data.tif
        """
    )
    
    parser.add_argument(
        '-g', '--geotiff',
        type=str,
        help='Path to GeoTIFF file to benchmark with real data',
        metavar='PATH'
    )
    
    args = parser.parse_args()
    
    geotiff_path = None
    if args.geotiff:
        geotiff_path = Path(args.geotiff)
        if not geotiff_path.exists():
            print(f"ERROR: File not found: {geotiff_path}")
            sys.exit(1)
    
    try:
        benchmark_slope_calculator(geotiff_path)
    except Exception as e:
        print(f"Error running benchmark: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()