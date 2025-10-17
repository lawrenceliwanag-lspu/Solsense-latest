"""
Main application coordinator class
Orchestrates all components and handles business logic
"""
import tkinter as tk
from tkinter import messagebox
import time
import numpy as np

from config.settings import APP_SETTINGS
from ui.styles import AppStyles
from ui.controls_panel import ControlsPanel
from ui.map_panel import MapPanel
from ui.info_bar import InfoBar
from ui.tutorial_dialog import TutorialDialog
from core.data_manager import DataManager
from core.geotiff_handler import GeoTIFFHandler
from core.slope_calculator import SlopeCalculator
from core.packing_solver import PackingSolver
from core.energy_estimator import EnergyEstimator
from services.file_service import FileService
from services.location_service import LocationService
from services.export_service import ExportService
from utils.animations import AnimationManager
from utils.conversions import ConversionUtils
from utils.validators import InputValidator

class GeoTIFFSlopeViewer:
    def __init__(self, master):
        self.master = master
        master.title(APP_SETTINGS['title'])
        master.geometry(APP_SETTINGS['geometry'])
        master.configure(bg='#f0f0f0')

        # Initialize styling
        self.styles = AppStyles()
        self.styles.setup_styles()

        # Initialize core components
        self.data_manager = DataManager()
        self.geotiff_handler = GeoTIFFHandler()
        self.slope_calculator = SlopeCalculator()
        self.packing_solver = PackingSolver()
        self.energy_estimator = EnergyEstimator()
        
        # Initialize services
        self.file_service = FileService()
        self.location_service = LocationService()
        self.export_service = ExportService()
        
        # Initialize utilities
        self.conversion_utils = ConversionUtils()
        self.input_validator = InputValidator()

        # Create main layout
        self.create_main_layout()

        # Initialize UI components with callbacks
        self.setup_ui_components()
        
        # Initialize animation manager after UI is created
        self.animation_manager = AnimationManager(
            self.map_panel.fig, 
            self.map_panel.ax, 
            self.map_panel.canvas
        )

    def create_main_layout(self):
        """Create the main layout structure"""
        # Main content area
        self.main_frame = tk.Frame(self.master, bg=self.styles.colors['background'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create main paned window
        self.main_pane = tk.PanedWindow(
            self.main_frame,
            orient=tk.HORIZONTAL,
            bg=self.styles.colors['background'],
            sashwidth=8,
            sashrelief=tk.FLAT
        )
        self.main_pane.pack(fill=tk.BOTH, expand=True)

    def setup_ui_components(self):
        """Initialize UI components with callback functions"""
        # Left panel container
        left_container = tk.Frame(self.main_pane, bg=self.styles.colors['background'], width=400)
        left_container.pack_propagate(False)
        self.main_pane.add(left_container, stretch="never")

        # Right panel for map
        right_frame = tk.Frame(self.main_pane, bg=self.styles.colors['surface'])
        self.main_pane.add(right_frame, stretch="always")

        # Create UI components with callbacks
        self.controls_panel = ControlsPanel(left_container, self.get_control_callbacks())
        self.map_panel = MapPanel(right_frame, self.get_map_callbacks())
        self.info_bar = InfoBar(self.map_panel.map_container, self.get_info_callbacks())
        
        # Store widget references for easy access
        self.controls = self.controls_panel.widgets
        self.info_widgets = self.info_bar.widgets

    def get_control_callbacks(self):
        """Return callback functions for control panel"""
        return {
            'load_geotiff': self.load_geotiff,
            'show_tutorial': self.show_tutorial,
            'clear_marker': self.clear_marker_and_packing,
            'unit_change': self.on_unit_change,
            'run_analysis': self.run_packing_and_energy_simulation,
            'export_results': self.export_results
        }

    def get_map_callbacks(self):
        """Return callback functions for map panel"""
        return {
            'map_click': self.on_click_map
        }

    def get_info_callbacks(self):
        """Return callback functions for info bar"""
        return {
            'update_location': self.update_location_name
        }

    def load_geotiff(self):
        """Load and process GeoTIFF file"""
        # Get file selection
        filepath = self.file_service.select_geotiff_file()
        if not filepath:
            return

        # Validate file
        is_valid, message = self.file_service.validate_file_exists(filepath)
        if not is_valid:
            self.file_service.show_file_error(message)
            return

        is_valid, message = self.file_service.validate_geotiff_extension(filepath)
        if not is_valid:
            self.file_service.show_file_error(message)
            return

        # Stop any existing animations
        self.animation_manager.stop_all_animations()
        
        # Clear existing data
        self.clear_all_data()
        
        # Start loading animation
        self.animation_manager.start_loading_animation(self.styles.colors)
        self.master.update()
        time.sleep(0.5)  # Show loading animation briefly

        try:
            # Load GeoTIFF
            geotiff_data = self.geotiff_handler.load_geotiff(filepath)
            
            # Validate loaded data
            is_valid, message = self.geotiff_handler.validate_geotiff(filepath)
            if not is_valid:
                self.animation_manager.stop_loading_animation()
                messagebox.showwarning("GeoTIFF Warning", message)
                # Continue anyway if possible
            
            # Store data in data manager
            self.data_manager.filepath = filepath
            self.data_manager.original_crs = geotiff_data['original_crs']
            self.data_manager.transform = geotiff_data['transform']
            self.data_manager.nodata_value = geotiff_data['nodata_value']
            self.data_manager.pixel_width_m = geotiff_data['pixel_width_m']
            self.data_manager.pixel_height_m = geotiff_data['pixel_height_m']
            
            # Calculate slope and aspect
            self.data_manager.slope_degrees, self.data_manager.aspect_degrees = \
                self.slope_calculator.calculate_slope_aspect_horn(
                    geotiff_data['dem_data'], 
                    geotiff_data['pixel_width_m'], 
                    geotiff_data['pixel_height_m']
                )
            
            # Create visualization
            self.data_manager.display_image_rgba = \
                self.slope_calculator.create_slope_visualization(
                    self.data_manager.slope_degrees,
                    self.data_manager.aspect_degrees,
                    self.data_manager.nodata_value
                )
            
            # Stop loading animation
            self.animation_manager.stop_loading_animation()
            
            # Update UI
            file_info = self.file_service.get_file_info(filepath)
            self.controls['lbl_file'].config(
                text=f"✓ {file_info['filename']} ({file_info['size_mb']} MB)",
                fg=self.styles.colors['success']
            )
            
            # Start data visualization animation
            self.animation_manager.start_data_reveal_animation(
                self.data_manager.display_image_rgba,
                self.styles.colors
            )
            
        except Exception as e:
            self.animation_manager.stop_loading_animation()
            self.file_service.show_file_error(f"Failed to load GeoTIFF: {e}")
            self.clear_all_data()

    def on_click_map(self, event):
        """Handle map click events"""
        if event.inaxes != self.map_panel.ax:
            return

        if not self.data_manager.is_data_loaded():
            return

        col, row = int(round(event.xdata)), int(round(event.ydata))
        
        # Clear previous marker before setting new one
        if self.data_manager.marker_object:
            self.map_panel.clear_marker(self.data_manager.marker_object)
            self.data_manager.marker_object = None
        
        # Store pixel coordinates
        self.data_manager.marker_pixel_coords = (col, row)
        
        # Convert to geographic coordinates
        try:
            lon, lat = self.conversion_utils.pixel_to_geographic(
                (col, row),
                self.data_manager.transform,
                self.data_manager.original_crs
            )
            self.data_manager.marker_lon_lat = (lon, lat)
            
            # Update UI
            self.controls['lbl_marker_coords'].config(
                text=f"Coordinates: {lon:.6f}, {lat:.6f}"
            )
            
            # Draw new marker
            self.data_manager.marker_object = self.map_panel.draw_marker((col, row))
            
            # Update info bar
            self.update_info_display()
            
            # Clear previous analysis results
            self.clear_analysis_results()
            
        except Exception as e:
            messagebox.showerror("Coordinate Error", f"Failed to get coordinates: {e}")
            self.data_manager.clear_marker()

    def on_unit_change(self, event=None):
        """Handle unit change in land dimensions"""
        unit = self.controls['land_unit'].get()
        
        if unit == "hectares":
            # Configure for hectares input
            self.controls['width_label'].config(text="Area (hectares):")
            self.controls['height_label'].config(text="Length/Depth (m):")
            self.controls['entry_land_height'].config(state='disabled')
            
            # Convert current values to hectares if possible
            try:
                current_width = float(self.controls['entry_land_width'].get())
                current_height = float(self.controls['entry_land_height'].get())
                area_hectares = (current_width * current_height) / 10000
                
                self.controls['entry_land_width'].delete(0, tk.END)
                self.controls['entry_land_width'].insert(0, f"{area_hectares:.3f}")
            except:
                self.controls['entry_land_width'].delete(0, tk.END)
                self.controls['entry_land_width'].insert(0, "0.5")
            
            self.controls['entry_land_height'].delete(0, tk.END)
            self.controls['entry_land_height'].insert(0, "N/A")
            
        else:  # meters
            # Configure for meters input
            self.controls['entry_land_height'].config(state='normal')
            self.controls['width_label'].config(text="Width (m):")
            self.controls['height_label'].config(text="Length/Depth (m):")
            
            # Convert hectares back to meters if possible
            try:
                area_hectares = float(self.controls['entry_land_width'].get())
                area_m2 = area_hectares * 10000
                # Create 2:1 ratio rectangle
                width_m = (area_m2 * 2) ** 0.5
                height_m = area_m2 / width_m
                
                self.controls['entry_land_width'].delete(0, tk.END)
                self.controls['entry_land_height'].delete(0, tk.END)
                self.controls['entry_land_width'].insert(0, f"{width_m:.0f}")
                self.controls['entry_land_height'].insert(0, f"{height_m:.0f}")
            except:
                self.controls['entry_land_width'].delete(0, tk.END)
                self.controls['entry_land_height'].delete(0, tk.END)
                self.controls['entry_land_width'].insert(0, "100")
                self.controls['entry_land_height'].insert(0, "50")

    def run_packing_and_energy_simulation(self):
        """Run solar panel packing and energy analysis"""
        # Validate prerequisites
        if not self.data_manager.is_marker_set():
            messagebox.showerror("Error", "Please click on the map to set a marker first.")
            return

        if not self.data_manager.is_data_loaded():
            messagebox.showerror("Error", "Please load a GeoTIFF file first.")
            return

        # Validate inputs
        packing_errors = self.input_validator.validate_packing_inputs(
            self.controls['entry_land_width'].get(),
            self.controls['entry_land_height'].get(),
            self.controls['entry_obj_width'].get(),
            self.controls['entry_obj_height'].get(),
            self.controls['land_unit'].get(),
            self.controls['entry_num_objects'].get() if self.controls['pack_mode'].get() == "specify" else None
        )

        energy_errors = self.input_validator.validate_energy_inputs(
            self.controls['entry_panel_efficiency'].get(),
            self.controls['entry_perf_ratio'].get()
        )

        all_errors = packing_errors + energy_errors
        if all_errors:
            messagebox.showerror("Input Validation Error", "\n".join(all_errors))
            return

        try:
            # Get validated inputs
            land_width_m, land_height_m = self.conversion_utils.convert_area_to_meters(
                self.controls['entry_land_width'].get(),
                self.controls['entry_land_height'].get(),
                self.controls['land_unit'].get()
            )

            panel_width_m = float(self.controls['entry_obj_width'].get())
            panel_height_m = float(self.controls['entry_obj_height'].get())
            
            num_to_pack = None
            if self.controls['pack_mode'].get() == "specify":
                num_to_pack = int(self.controls['entry_num_objects'].get())

            # Run packing algorithm
            packed_objects = self.packing_solver.next_fit_shelf_packing(
                land_width_m, land_height_m, panel_width_m, panel_height_m, num_to_pack
            )

            num_panels_packed = len(packed_objects)
            
            # Update data manager
            self.data_manager.num_panels_packed = num_panels_packed
            self.data_manager.land_area_m2 = land_width_m * land_height_m

            if num_panels_packed == 0:
                status_msg = "No panels could be packed."
                if num_to_pack is not None:
                    status_msg = f"Could not pack the specified {num_to_pack} panels."
                self.controls['lbl_panels_packed'].config(text=status_msg)
                self.controls['lbl_annual_energy'].config(text="⚡ Annual Energy: 0 kWh")
                self.update_info_display()
                return

            # Update packing results
            status_msg = f"📦 Panels Packed: {num_panels_packed}"
            if num_to_pack is not None and num_panels_packed < num_to_pack:
                status_msg += f" (Requested: {num_to_pack})"
            self.controls['lbl_panels_packed'].config(text=status_msg)

            # Calculate energy production
            self.calculate_energy_production(num_panels_packed, panel_width_m * panel_height_m)
            
            # Update info display
            self.update_info_display()

        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to run analysis: {e}")

    def calculate_energy_production(self, num_panels, panel_area_m2):
        """Calculate and display energy production estimates"""
        if not self.data_manager.marker_lon_lat:
            self.controls['lbl_annual_energy'].config(text="⚡ Annual Energy: Set marker first")
            return

        try:
            # Get energy parameters
            panel_efficiency = float(self.controls['entry_panel_efficiency'].get()) / 100.0
            performance_ratio = float(self.controls['entry_perf_ratio'].get())
            
            # Fetch solar irradiance data
            self.controls['lbl_annual_energy'].config(text="⚡ Annual Energy: Fetching solar data...")
            self.master.update_idletasks()
            
            lon, lat = self.data_manager.marker_lon_lat
            avg_daily_irradiance = self.energy_estimator.fetch_solar_irradiance(lon, lat)
            
            # Calculate energy production
            energy_data = self.energy_estimator.calculate_energy_production(
                num_panels, panel_area_m2, panel_efficiency, performance_ratio, avg_daily_irradiance
            )
            
            # Update data manager
            self.data_manager.annual_energy_kwh = energy_data['annual_energy_kwh']
            self.data_manager.daily_energy_kwh = energy_data['daily_energy_kwh']
            
            # Update UI
            self.controls['lbl_annual_energy'].config(
                text=f"⚡ Annual Energy: {energy_data['annual_energy_kwh']:,.2f} kWh"
            )
            
        except Exception as e:
            self.controls['lbl_annual_energy'].config(text="⚡ Annual Energy: Data unavailable")
            messagebox.showerror("Energy Calculation Error", f"Failed to calculate energy: {e}")

    def update_location_name(self):
        """Update location name using reverse geocoding"""
        if not self.data_manager.marker_lon_lat:
            messagebox.showwarning("Location Update", "Set a marker first.")
            return
        
        # Show loading state
        original_text = self.info_widgets['info_location_name'].cget("text")
        self.info_widgets['info_location_name'].config(text="Loading...")
        self.master.update_idletasks()
        
        try:
            lon, lat = self.data_manager.marker_lon_lat
            location_name = self.location_service.reverse_geocode(lon, lat)
            self.data_manager.location_name = location_name
            self.info_widgets['info_location_name'].config(text=location_name)
        except Exception as e:
            self.info_widgets['info_location_name'].config(text=original_text)
            messagebox.showerror("Location Error", f"Failed to fetch location: {e}")

    def export_results(self):
        """Export analysis results to CSV"""
        if not self.data_manager.is_marker_set():
            messagebox.showwarning("Export", "No analysis data to export.")
            return
        
        try:
            success = self.export_service.export_analysis_results(
                self.data_manager, self.slope_calculator
            )
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {e}")

    def show_tutorial(self, event=None):
        """Show tutorial dialog"""
        tutorial = TutorialDialog(self.master)
        tutorial.show_tutorial()

    def clear_marker_and_packing(self):
        """Clear marker and packing visualizations"""
        # Clear marker visualization
        if self.data_manager.marker_object:
            self.map_panel.clear_marker(self.data_manager.marker_object)
        
        # Clear data
        self.data_manager.clear_marker()
        self.data_manager.clear_analysis_results()
        
        # Update UI
        self.controls['lbl_marker_coords'].config(text="Coordinates: Not set")
        self.clear_analysis_results()
        self.update_info_display()

    def clear_analysis_results(self):
        """Clear analysis results from UI"""
        self.controls['lbl_panels_packed'].config(text="📦 Panels Packed: Not calculated")
        self.controls['lbl_annual_energy'].config(text="⚡ Annual Energy: Not calculated")

    def clear_all_data(self):
        """Clear all data and reset UI"""
        self.data_manager.clear_data()
        self.data_manager.clear_marker()
        self.data_manager.clear_analysis_results()
        
        self.map_panel.clear_display()
        self.controls['lbl_file'].config(text="No file loaded", fg=self.styles.colors['text_secondary'])
        self.controls['lbl_marker_coords'].config(text="Coordinates: Not set")
        self.clear_analysis_results()
        self.info_bar.reset_display()

    def update_info_display(self):
        """Update the information bar with current data"""
        # Update panels count
        self.info_bar.update_panels_count(self.data_manager.num_panels_packed)
        
        # Update energy values
        self.info_bar.update_energy_values(
            self.data_manager.daily_energy_kwh,
            self.data_manager.annual_energy_kwh
        )
        
        # Update coordinates and location
        if self.data_manager.marker_lon_lat:
            lon, lat = self.data_manager.marker_lon_lat
            self.info_bar.update_coordinates(lon, lat)
            self.info_bar.update_location_name(self.data_manager.location_name)
            self.info_bar.update_land_size(self.data_manager.land_area_m2)