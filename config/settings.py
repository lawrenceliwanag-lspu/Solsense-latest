"""
Application configuration and constants
"""

# Color scheme
COLORS = {
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'secondary': '#FF9800',
    'success': '#4CAF50',
    'warning': '#FF5722',
    'background': '#fafafa',
    'surface': '#ffffff',
    'text_primary': '#212121',
    'text_secondary': '#757575',
    'border': '#e0e0e0',
    'transparent': "#f8f8f800",
    'surface_elevated': '#ffffff',
    'accent': "#FFFFFF"
}

# Default values
DEFAULT_VALUES = {
    'land_width': '100',
    'land_height': '50',
    'panel_width': '1.65',
    'panel_height': '1.0',
    'panel_efficiency': '18',
    'performance_ratio': '0.8',
    'num_objects': '10',
    'hectares_area': '0.5'
}

# Application settings
APP_SETTINGS = {
    'title': "SolSense: GeoTIFF Slope Viewer",
    'geometry': "1200x900",
    'min_slope_threshold': 5.0,
    'max_packing_iterations': 1_000_000,
    'animation_interval': 100,
    'data_reveal_interval': 50
}

# API settings
API_SETTINGS = {
    'nasa_power_base_url': "https://power.larc.nasa.gov/api/temporal/climatology/point",
    'nominatim_base_url': "https://nominatim.openstreetmap.org/reverse",
    'request_timeout': 15,
    'cache_size': 32
}

# File paths
RESOURCE_PATHS = {
    'splash_image': "resources/splash.png",
    'interface_bg': "resources/interface_bg.png"
}