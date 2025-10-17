"""
Data export services
"""
import csv
from datetime import datetime, timezone
from tkinter import filedialog, messagebox
import numpy as np

class ExportService:
    def __init__(self):
        pass
    
    def export_analysis_results(self, data_manager, slope_calculator):
        """Export analysis results to CSV file"""
        if not data_manager.is_marker_set():
            messagebox.showwarning("Export", "No analysis data to export. Run an analysis first.")
            return False
        
        # Get save file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Analysis Results"
        )
        
        if not file_path:
            return False
        
        try:
            # Get slope and aspect data at marker location
            slope, aspect = data_manager.get_marker_slope_aspect()
            direction = slope_calculator.get_aspect_direction(aspect) if aspect is not None else "NoData"
            
            # Write CSV file
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    "Timestamp",
                    "Longitude", 
                    "Latitude",
                    "Location_Name",
                    "Slope_Degrees", 
                    "Aspect_Direction",
                    "Num_Panels",
                    "Annual_Energy_kWh",
                    "Daily_Energy_kWh",
                    "Land_Area_m2"
                ])
                
                # Write data
                lon, lat = data_manager.marker_lon_lat
                writer.writerow([
                    datetime.now(timezone.utc).isoformat(timespec='seconds'),
                    f"{lon:.6f}",
                    f"{lat:.6f}", 
                    data_manager.location_name,
                    f"{slope:.2f}" if slope is not None and not np.isnan(slope) else "NoData",
                    direction,
                    data_manager.num_panels_packed,
                    f"{data_manager.annual_energy_kwh:.2f}",
                    f"{data_manager.daily_energy_kwh:.2f}",
                    f"{data_manager.land_area_m2:.2f}"
                ])
            
            messagebox.showinfo("Export Complete", f"Analysis results saved to:\n{file_path}")
            return True
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{e}")
            return False
    
    def export_packed_objects(self, packed_objects, file_path=None):
        """Export packed object coordinates to CSV"""
        if not packed_objects:
            messagebox.showwarning("Export", "No packed objects to export.")
            return False
        
        if not file_path:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Export Packed Objects"
            )
        
        if not file_path:
            return False
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Object_ID", "X_meters", "Y_meters", "Width_meters", "Height_meters"])
                
                for i, obj in enumerate(packed_objects, 1):
                    writer.writerow([
                        i,
                        f"{obj['x']:.3f}",
                        f"{obj['y']:.3f}", 
                        f"{obj['w']:.3f}",
                        f"{obj['h']:.3f}"
                    ])
            
            messagebox.showinfo("Export Complete", f"Packed objects saved to:\n{file_path}")
            return True
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export packed objects:\n{e}")
            return False