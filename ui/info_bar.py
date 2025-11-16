"""
Information bar component at bottom of map
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from config.settings import COLORS, FONT_SIZES

class InfoBar:
    def __init__(self, parent_frame, app_callbacks):
        self.parent_frame = parent_frame
        self.callbacks = app_callbacks
        self.colors = COLORS
        self.fonts = FONT_SIZES
        
        # Create info bar
        self._create_info_bar()
        
        # Store widget references
        self.widgets = self._collect_widget_references()
    
    def _create_info_bar(self):
        """Create the information bar below the map"""
        info_bar_frame = tk.Frame(self.parent_frame, bg=self.colors['surface'])
        info_bar_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Main container with 4 sections
        sections_frame = tk.Frame(info_bar_frame, bg=self.colors['surface'])
        sections_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Create sections
        self._create_panels_section(sections_frame)
        self._create_energy_section(sections_frame)
        self._create_coordinates_section(sections_frame)
        self._create_legend_section(sections_frame)
    
    def _load_icon(self, icon_path, size=(64, 64)):
        """Load and resize icon from res folder"""
        try:
            image = Image.open(icon_path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading icon {icon_path}: {e}")
            return None
    
    def _create_panels_section(self, parent):
        """Section 1: Placeable Solar Panels"""
        panel_section = tk.Frame(parent, bg=self.colors['surface'])
        panel_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Heading
        panel_heading = tk.Label(panel_section, text="PLACEABLE SOLAR PANELS", 
                               font=('Segoe UI', self.fonts['body_small'], 'bold'), fg=self.colors['text_secondary'],
                               bg=self.colors['surface'])
        panel_heading.pack(fill=tk.X, pady=(0, 5))
        
        # Content frame with icon and info side by side
        content_frame = tk.Frame(panel_section, bg=self.colors['surface'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon frame
        icon_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        icon_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Load solar panel icon
        panel_icon_img = self._load_icon("resources/solar_panels.jpg", size=(100, 100))
        panel_icon = tk.Label(icon_frame, image=panel_icon_img if panel_icon_img else None,
                            text="☀️" if not panel_icon_img else "",
                            font=('Segoe UI', self.fonts['icon_text']) if not panel_icon_img else None,
                            bg=self.colors['surface'], fg=self.colors['text_primary'])
        panel_icon.pack(expand=True)
        if panel_icon_img:
            panel_icon.image = panel_icon_img  # Keep a reference
        
        # Info frame
        info_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.info_panels_count = tk.Label(info_frame, text="0", 
                                        font=('Segoe UI', self.fonts['display'], 'bold'), 
                                        fg=self.colors['text_primary'],
                                        bg=self.colors['surface'])
        self.info_panels_count.pack(anchor='w')
    
    def _create_energy_section(self, parent):
        """Section 2: Electricity Generation"""
        energy_section = tk.Frame(parent, bg=self.colors['surface'])
        energy_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Heading
        energy_heading = tk.Label(energy_section, text="ELECTRICITY GENERATION", 
                                font=('Segoe UI', self.fonts['body_small'], 'bold'), fg=self.colors['text_secondary'],
                                bg=self.colors['surface'])
        energy_heading.pack(fill=tk.X, pady=(0, 5))
        
        # Content frame with icon and info side by side
        content_frame = tk.Frame(energy_section, bg=self.colors['surface'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon frame
        icon_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        icon_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Load energy icon
        energy_icon_img = self._load_icon("resources/electricity.jpg", size=(100, 100))
        energy_icon = tk.Label(icon_frame, image=energy_icon_img if energy_icon_img else None,
                             text="⚡" if not energy_icon_img else "",
                             font=('Segoe UI', self.fonts['icon_text']) if not energy_icon_img else None,
                             bg=self.colors['surface'], fg=self.colors['text_primary'])
        energy_icon.pack(expand=True)
        if energy_icon_img:
            energy_icon.image = energy_icon_img  # Keep a reference
        
        # Info frame
        info_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Metric units label
        metric_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        metric_frame.pack(anchor='w')
        
        tk.Label(metric_frame, text="Metric Units", font=('Segoe UI', self.fonts['body_xsmall']), 
                fg=self.colors['text_secondary'], bg=self.colors['surface']).pack(side=tk.LEFT)
        tk.Label(metric_frame, text="●", font=('Segoe UI', self.fonts['body_small']), 
                fg=self.colors['primary'], bg=self.colors['surface']).pack(side=tk.LEFT, padx=(5,0))
        tk.Label(metric_frame, text="kWh", font=('Segoe UI', self.fonts['body_xsmall']), 
                fg=self.colors['primary'], bg=self.colors['surface']).pack(side=tk.LEFT, padx=(2,0))
        
        # Daily energy
        daily_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        daily_frame.pack(anchor='w')
        
        tk.Label(daily_frame, text="Daily", font=('Segoe UI', self.fonts['body_small'], 'bold'), 
                fg=self.colors['text_primary'], bg=self.colors['surface']).pack(side=tk.LEFT)
        self.info_daily_energy = tk.Label(daily_frame, text="0.00", 
                                        font=('Segoe UI', self.fonts['body_small'], 'bold'), 
                                        fg=self.colors['text_primary'],
                                        bg=self.colors['surface'])
        self.info_daily_energy.pack(side=tk.LEFT, padx=(5,0))
        
        # Annual energy
        annual_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        annual_frame.pack(anchor='w')
        
        tk.Label(annual_frame, text="Annually", font=('Segoe UI', self.fonts['body_small'], 'bold'), 
                fg=self.colors['text_primary'], bg=self.colors['surface']).pack(side=tk.LEFT)
        self.info_annual_energy = tk.Label(annual_frame, text="0.00", 
                                        font=('Segoe UI', self.fonts['body_small'], 'bold'), 
                                        fg=self.colors['text_primary'],
                                        bg=self.colors['surface'])
        self.info_annual_energy.pack(side=tk.LEFT, padx=(5,0))
    
    def _create_coordinates_section(self, parent):
        """Section 3: Marked Coordinates"""
        coord_section = tk.Frame(parent, bg=self.colors['surface'])
        coord_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Heading
        coord_heading = tk.Label(coord_section, text="MARKED COORDINATES", 
                               font=('Segoe UI', self.fonts['body_small'], 'bold'), fg=self.colors['text_secondary'],
                               bg=self.colors['surface'])
        coord_heading.pack(fill=tk.X, pady=(0, 5))
        
        # Content frame with icon and info side by side
        content_frame = tk.Frame(coord_section, bg=self.colors['surface'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon frame
        icon_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        icon_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Load coordinates icon
        coord_icon_img = self._load_icon("resources/coordinate.jpg", size=(100, 100))
        coord_icon = tk.Label(icon_frame, image=coord_icon_img if coord_icon_img else None,
                            text="📍" if not coord_icon_img else "",
                            font=('Segoe UI', self.fonts['icon_text']) if not coord_icon_img else None,
                            bg=self.colors['surface'], fg=self.colors['text_primary'])
        coord_icon.pack(expand=True)
        if coord_icon_img:
            coord_icon.image = coord_icon_img  # Keep a reference
        
        # Info frame
        info_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Location name section
        location_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        location_frame.pack(anchor='w', fill=tk.X)

        # tk.Label(location_frame, text="Precise Location", font=('Segoe UI', self.fonts['body_xsmall']), 
        #         fg=self.colors['text_secondary'], bg=self.colors['surface']).pack(anchor='w')

        # Location name and update button
        name_button_frame = tk.Frame(location_frame, bg=self.colors['surface'])
        name_button_frame.pack(anchor='w')

        self.info_location_name = tk.Label(name_button_frame, text="Not Set", 
                                        font=('Segoe UI', self.fonts['body_medium'], 'bold'), 
                                        fg=self.colors['text_primary'],
                                        bg=self.colors['surface'])
        self.info_location_name.pack(side=tk.LEFT)

        self.btn_update_location = ttk.Button(name_button_frame, text="🔄", 
                                            width=3,
                                            command=self.callbacks['update_location'])
        self.btn_update_location.pack(side=tk.LEFT, padx=(5,0))
        
        # Coordinates
        coords_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        coords_frame.pack(anchor='w')
        
        tk.Label(coords_frame, text="Longitude", font=('Segoe UI', self.fonts['body_xsmall']), 
                fg=self.colors['text_secondary'], bg=self.colors['surface']).pack(side=tk.LEFT)
        self.info_longitude = tk.Label(coords_frame, text="0.0000°", 
                                    font=('Segoe UI', self.fonts['body_small']), 
                                    fg=self.colors['text_primary'],
                                    bg=self.colors['surface'])
        self.info_longitude.pack(side=tk.LEFT, padx=(5,0))
        
        coords_frame2 = tk.Frame(info_frame, bg=self.colors['surface'])
        coords_frame2.pack(anchor='w')
        
        tk.Label(coords_frame2, text="Latitude", font=('Segoe UI', self.fonts['body_xsmall']), 
                fg=self.colors['text_secondary'], bg=self.colors['surface']).pack(side=tk.LEFT)
        self.info_latitude = tk.Label(coords_frame2, text="0.0000°", 
                                    font=('Segoe UI', self.fonts['body_small']), 
                                    fg=self.colors['text_primary'],
                                    bg=self.colors['surface'])
        self.info_latitude.pack(side=tk.LEFT, padx=(5,0))
        
        # Land size
        land_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        land_frame.pack(anchor='w')
        
        tk.Label(land_frame, text="Land Size", font=('Segoe UI', self.fonts['body_xsmall']), 
                fg=self.colors['text_secondary'], bg=self.colors['surface']).pack(side=tk.LEFT)
        self.info_land_size = tk.Label(land_frame, text="0 m²", 
                                    font=('Segoe UI', self.fonts['body_small'], 'bold'), 
                                    fg=self.colors['text_primary'],
                                    bg=self.colors['surface'])
        self.info_land_size.pack(side=tk.LEFT, padx=(5,0))
    
    def _create_legend_section(self, parent):
        """Section 4: Land Suitability Legend"""
        legend_section = tk.Frame(parent, bg=self.colors['surface'])
        legend_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Heading
        legend_heading = tk.Label(legend_section, text="LAND SUITABILITY LEGEND", 
                                font=('Segoe UI', self.fonts['body_small'], 'bold'), fg=self.colors['text_secondary'],
                                bg=self.colors['surface'])
        legend_heading.pack(fill=tk.X, pady=(0, 5))
        
        # Content frame
        content_frame = tk.Frame(legend_section, bg=self.colors['surface'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Legend items
        legend_items = [
            ("■", '#00AA00', "Highly Suitable"),
            ("■", "#F1F100", "Moderately Suitable"),
            ("■", '#808080', "Unsuitable"),
            ("●", "#DB1414", "Loc. Marker")
        ]
        
        for symbol, color, label in legend_items:
            item_frame = tk.Frame(content_frame, bg=self.colors['surface'])
            item_frame.pack(anchor='w', pady=2)
            
            symbol_size = 12 if symbol == "■" else 12
            tk.Label(item_frame, text=f"{symbol} ", font=('Segoe UI', symbol_size), 
                    fg=color, bg=self.colors['surface']).pack(side=tk.LEFT)
            tk.Label(item_frame, text=label, font=('Segoe UI', self.fonts['body_small']), 
                    fg=self.colors['text_primary'], bg=self.colors['surface']).pack(side=tk.LEFT, padx=(5,0))
    
    def _collect_widget_references(self):
        """Collect widget references for external access"""
        return {
            'info_panels_count': self.info_panels_count,
            'info_daily_energy': self.info_daily_energy,
            'info_annual_energy': self.info_annual_energy,
            'info_location_name': self.info_location_name,
            'btn_update_location': self.btn_update_location,
            'info_longitude': self.info_longitude,
            'info_latitude': self.info_latitude,
            'info_land_size': self.info_land_size
        }
    
    def update_panels_count(self, count):
        """Update panels count display"""
        self.info_panels_count.config(text=str(count))
    
    def update_energy_values(self, daily_kwh, annual_kwh):
        """Update energy values display"""
        self.info_daily_energy.config(text=f"{daily_kwh:.2f}")
        self.info_annual_energy.config(text=f"{annual_kwh:,.0f}")
    
    def update_coordinates(self, lon, lat):
        """Update coordinate display"""
        self.info_longitude.config(text=f"{lon:.4f}°")
        self.info_latitude.config(text=f"{lat:.4f}°")
    
    def update_location_name(self, name):
        """Update location name display"""
        self.info_location_name.config(text=name)
    
    def update_land_size(self, area_m2):
        """Update land size display"""
        self.info_land_size.config(text=f"{area_m2:,.0f} m²")
    
    def reset_display(self):
        """Reset all displays to default values"""
        self.info_panels_count.config(text="0")
        self.info_daily_energy.config(text="0.00")
        self.info_annual_energy.config(text="0.00")
        self.info_longitude.config(text="0.0000°")
        self.info_latitude.config(text="0.0000°")
        self.info_location_name.config(text="Not Set")
        self.info_land_size.config(text="0 m²")