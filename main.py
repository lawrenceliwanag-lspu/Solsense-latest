"""
SolSense: GeoTIFF Slope Viewer
Main entry point for the application
"""
import tkinter as tk
import time
from ui.splash import SplashScreen
from app import GeoTIFFSlopeViewer

if __name__ == "__main__":
    # Show splash screen
    splash = SplashScreen()
    
    # Update splash status with delays
    splash.update_status("Loading libraries...")
    splash.splash.update()
    time.sleep(0.8)
    
    splash.update_status("Initializing interface...")
    splash.splash.update()
    time.sleep(0.6)
    
    splash.update_status("Preparing map components...")
    splash.splash.update()
    time.sleep(0.6)
    
    splash.update_status("Starting SolSense...")
    splash.splash.update()
    time.sleep(0.5)
    
    # Close splash screen
    splash.close()
    
    # Create and run main application
    root = tk.Tk()
    app = GeoTIFFSlopeViewer(root)
    root.bind_all("<Control-o>", lambda e: app.load_geotiff())
    root.bind_all("<Control-r>", lambda e: app.run_packing_and_energy_simulation())
    root.bind_all("<Control-q>", lambda e: root.quit())
    root.mainloop()