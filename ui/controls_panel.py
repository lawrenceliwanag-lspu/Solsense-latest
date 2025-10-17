"""
Left control panel with file loading, packing, and results sections
"""
import tkinter as tk
from tkinter import ttk
from config.settings import COLORS, DEFAULT_VALUES

class ControlsPanel:
    def __init__(self, parent_frame, app_callbacks):
        self.parent_frame = parent_frame
        self.callbacks = app_callbacks
        self.colors = COLORS
        self.defaults = DEFAULT_VALUES
        
        # Create scrollable container
        self._create_scrollable_container()
        
        # Create sections
        self._create_file_section()
        self._create_packing_section()
        self._create_results_section()
        
        # Store widget references for external access
        self.widgets = self._collect_widget_references()
    
    def _create_scrollable_container(self):
        """Create scrollable container for controls"""
        canvas_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.controls_canvas = tk.Canvas(
            canvas_frame,
            bg=self.colors['background'],
            highlightthickness=0,
            borderwidth=0
        )

        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.controls_canvas.yview)
        self.scrollable_frame = tk.Frame(self.controls_canvas, bg=self.colors['background'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.controls_canvas.configure(scrollregion=self.controls_canvas.bbox("all"))
        )

        self.controls_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.controls_canvas.configure(yscrollcommand=scrollbar.set)

        self.controls_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_file_section(self):
        """Create file loading section"""
        file_frame = ttk.Labelframe(
            self.scrollable_frame,
            text="📁 GeoTIFF File",
            style='Modern.TLabelframe',
            padding="15"
        )
        file_frame.pack(fill=tk.X, pady=(0, 15), padx=10)

        # Load button
        self.btn_load = ttk.Button(
            file_frame,
            text="📂 Load GeoTIFF File",
            style='Primary.TButton',
            command=self.callbacks['load_geotiff']
        )
        self.btn_load.pack(pady=(0, 0), fill=tk.X)

        # Tutorial link
        tutorial_link = tk.Label(
            file_frame,
            text="Need help? How to get GeoTIFF files",
            bg=self.colors['surface'],
            fg=self.colors['primary'],
            font=('Segoe UI', 8, 'underline'),
            cursor='hand2'
        )
        tutorial_link.pack(pady=(5, 0))
        tutorial_link.bind('<Button-1>', self.callbacks['show_tutorial'])

        # File info
        self.lbl_file = tk.Label(
            file_frame,
            text="No file loaded",
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            font=('Segoe UI', 9)
        )
        self.lbl_file.pack(pady=(0, 0))
    
    def _create_packing_section(self):
        """Create packing and energy analysis section"""
        pack_frame = ttk.Labelframe(
            self.scrollable_frame,
            text="⚡ Solar Panel Analysis",
            style='Modern.TLabelframe',
            padding="15"
        )
        pack_frame.pack(fill=tk.X, pady=(0, 15), padx=10)

        # Marker section
        self._create_marker_subsection(pack_frame)
        self._add_separator(pack_frame)
        
        # Land dimensions section
        self._create_land_dimensions_subsection(pack_frame)
        self._add_separator(pack_frame)
        
        # Panel specifications section
        self._create_panel_specs_subsection(pack_frame)
        self._add_separator(pack_frame)
        
        # Performance parameters section
        self._create_performance_subsection(pack_frame)
        self._add_separator(pack_frame)
        
        # Run analysis button
        self.btn_run_packing = ttk.Button(
            pack_frame,
            text="🔄 Run Analysis",
            style='Secondary.TButton',
            command=self.callbacks['run_analysis']
        )
        self.btn_run_packing.pack(pady=(5, 0), fill=tk.X)
    
    def _create_marker_subsection(self, parent):
        """Create marker section"""
        marker_section = tk.Frame(parent, bg=self.colors['surface'])
        marker_section.pack(fill=tk.X, pady=(0, 15))

        marker_title = tk.Label(
            marker_section,
            text="📍 Location Marker",
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 9, 'bold')
        )
        marker_title.pack(anchor=tk.W, pady=(0, 5))

        self.lbl_marker_coords = tk.Label(
            marker_section,
            text="Coordinates: Not set",
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            font=('Segoe UI', 8)
        )
        self.lbl_marker_coords.pack(anchor=tk.W)

        ttk.Button(
            marker_section, 
            text="🧹 Clear", 
            style='Secondary.TButton',
            command=self.callbacks['clear_marker']
        ).pack(anchor='e', pady=(0, 5))
    
    def _create_land_dimensions_subsection(self, parent):
        """Create land dimensions section"""
        land_section = tk.Frame(parent, bg=self.colors['surface'])
        land_section.pack(fill=tk.X, pady=(0, 15))

        land_title = tk.Label(
            land_section,
            text="🏞️ Land Dimensions",
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 9, 'bold')
        )
        land_title.pack(anchor=tk.W, pady=(0, 10))

        # Unit selection
        unit_frame = tk.Frame(land_section, bg=self.colors['surface'])
        unit_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(unit_frame, text="Unit:", bg=self.colors['surface'],
                fg=self.colors['text_primary'], font=('Segoe UI', 8)).pack(side=tk.LEFT)
        self.land_unit = ttk.Combobox(
            unit_frame, 
            style='Modern.TEntry', 
            width=12,
            values=["meters", "hectares"], 
            state="readonly"
        )
        self.land_unit.set("meters")
        self.land_unit.pack(side=tk.RIGHT)
        self.land_unit.bind('<<ComboboxSelected>>', self.callbacks['unit_change'])

        # Width input
        width_frame = tk.Frame(land_section, bg=self.colors['surface'])
        width_frame.pack(fill=tk.X, pady=(0, 8))
        self.width_label = tk.Label(width_frame, text="Width (m):", bg=self.colors['surface'],
                fg=self.colors['text_primary'], font=('Segoe UI', 8))
        self.width_label.pack(side=tk.LEFT)
        self.entry_land_width = ttk.Entry(width_frame, style='Modern.TEntry', width=15)
        self.entry_land_width.insert(0, self.defaults['land_width'])
        self.entry_land_width.pack(side=tk.RIGHT)

        # Height input
        height_frame = tk.Frame(land_section, bg=self.colors['surface'])
        height_frame.pack(fill=tk.X, pady=(0, 8))
        self.height_label = tk.Label(height_frame, text="Length/Depth (m):", bg=self.colors['surface'],
                fg=self.colors['text_primary'], font=('Segoe UI', 8))
        self.height_label.pack(side=tk.LEFT)
        self.entry_land_height = ttk.Entry(height_frame, style='Modern.TEntry', width=15)
        self.entry_land_height.insert(0, self.defaults['land_height'])
        self.entry_land_height.pack(side=tk.RIGHT)
    
    def _create_panel_specs_subsection(self, parent):
        """Create panel specifications section"""
        panel_section = tk.Frame(parent, bg=self.colors['surface'])
        panel_section.pack(fill=tk.X, pady=(0, 15))

        panel_title = tk.Label(
            panel_section,
            text="☀️ Panel Specifications",
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 9, 'bold')
        )
        panel_title.pack(anchor=tk.W, pady=(0, 10))

        # Panel dimensions
        panel_width_frame = tk.Frame(panel_section, bg=self.colors['surface'])
        panel_width_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(panel_width_frame, text="Panel Width (m):", bg=self.colors['surface'],
                fg=self.colors['text_primary'], font=('Segoe UI', 8)).pack(side=tk.LEFT)
        self.entry_obj_width = ttk.Entry(panel_width_frame, style='Modern.TEntry', width=15)
        self.entry_obj_width.insert(0, self.defaults['panel_width'])
        self.entry_obj_width.pack(side=tk.RIGHT)

        panel_height_frame = tk.Frame(panel_section, bg=self.colors['surface'])
        panel_height_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(panel_height_frame, text="Panel Height (m):", bg=self.colors['surface'],
                fg=self.colors['text_primary'], font=('Segoe UI', 8)).pack(side=tk.LEFT)
        self.entry_obj_height = ttk.Entry(panel_height_frame, style='Modern.TEntry', width=15)
        self.entry_obj_height.insert(0, self.defaults['panel_height'])
        self.entry_obj_height.pack(side=tk.RIGHT)

        # Packing mode
        self._create_packing_mode_subsection(panel_section)
    
    def _create_packing_mode_subsection(self, parent):
        """Create packing mode selection"""
        pack_mode_frame = tk.Frame(parent, bg=self.colors['surface'])
        pack_mode_frame.pack(fill=tk.X, pady=(10, 0))

        self.pack_mode = tk.StringVar(value="fill")

        mode_title = tk.Label(
            pack_mode_frame,
            text="Packing Mode:",
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 8, 'bold')
        )
        mode_title.pack(anchor=tk.W, pady=(0, 5))

        radio_frame = tk.Frame(pack_mode_frame, bg=self.colors['surface'])
        radio_frame.pack(fill=tk.X)

        tk.Radiobutton(
            radio_frame, 
            text="Fill maximum panels",
            variable=self.pack_mode, 
            value="fill",
            bg=self.colors['surface'], 
            fg=self.colors['text_primary'],
            font=('Segoe UI', 8), 
            selectcolor=self.colors['accent']
        ).pack(anchor=tk.W)

        tk.Radiobutton(
            radio_frame, 
            text="Specify number:",
            variable=self.pack_mode, 
            value="specify",
            bg=self.colors['surface'], 
            fg=self.colors['text_primary'],
            font=('Segoe UI', 8), 
            selectcolor=self.colors['accent']
        ).pack(anchor=tk.W)

        num_frame = tk.Frame(radio_frame, bg=self.colors['surface'])
        num_frame.pack(fill=tk.X, padx=20)
        tk.Label(num_frame, text="Number:", bg=self.colors['surface'],
                fg=self.colors['text_primary'], font=('Segoe UI', 8)).pack(side=tk.LEFT)
        self.entry_num_objects = ttk.Entry(num_frame, style='Modern.TEntry', width=10)
        self.entry_num_objects.insert(0, self.defaults['num_objects'])
        self.entry_num_objects.pack(side=tk.RIGHT)
    
    def _create_performance_subsection(self, parent):
        """Create performance parameters section"""
        perf_section = tk.Frame(parent, bg=self.colors['surface'])
        perf_section.pack(fill=tk.X, pady=(0, 15))

        perf_title = tk.Label(
            perf_section,
            text="⚙️ Performance Parameters",
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 9, 'bold')
        )
        perf_title.pack(anchor=tk.W, pady=(0, 10))

        # Efficiency
        eff_frame = tk.Frame(perf_section, bg=self.colors['surface'])
        eff_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(eff_frame, text="Panel Efficiency (%):", bg=self.colors['surface'],
                fg=self.colors['text_primary'], font=('Segoe UI', 8)).pack(side=tk.LEFT)
        self.entry_panel_efficiency = ttk.Entry(eff_frame, style='Modern.TEntry', width=15)
        self.entry_panel_efficiency.insert(0, self.defaults['panel_efficiency'])
        self.entry_panel_efficiency.pack(side=tk.RIGHT)

        # Performance ratio
        ratio_frame = tk.Frame(perf_section, bg=self.colors['surface'])
        ratio_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(ratio_frame, text="Performance Ratio:", bg=self.colors['surface'],
                fg=self.colors['text_primary'], font=('Segoe UI', 8)).pack(side=tk.LEFT)
        self.entry_perf_ratio = ttk.Entry(ratio_frame, style='Modern.TEntry', width=15)
        self.entry_perf_ratio.insert(0, self.defaults['performance_ratio'])
        self.entry_perf_ratio.pack(side=tk.RIGHT)
    
    def _create_results_section(self):
        """Create results display section"""
        results_frame = ttk.Labelframe(
            self.scrollable_frame,
            text="Miscellaneous",
            style='Modern.TLabelframe',
            padding="15"
        )
        results_frame.pack(fill=tk.X, pady=(0, 15), padx=10)

        # Results container
        self.results_container = tk.Frame(results_frame, bg=self.colors['surface'])
        self.results_container.pack(fill=tk.X)

        # Results labels
        self.lbl_panels_packed = tk.Label(
            self.results_container,
            text="📦 Panels Packed: Not calculated",
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            font=('Segoe UI', 9)
        )
        self.lbl_panels_packed.pack(anchor=tk.W, pady=(0, 8))

        self.lbl_annual_energy = tk.Label(
            self.results_container,
            text="⚡ Annual Energy: Not calculated",
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            font=('Segoe UI', 9)
        )
        self.lbl_annual_energy.pack(anchor=tk.W, pady=(0, 8))

        # Export button
        ttk.Button(
            self.results_container, 
            text="💾 Export CSV",
            command=self.callbacks['export_results']
        ).pack(anchor='e', pady=(10, 0))

        # Additional stats
        self.lbl_additional_stats = tk.Label(
            self.results_container,
            text="",
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            font=('Segoe UI', 8)
        )
        self.lbl_additional_stats.pack(anchor=tk.W)
    
    def _add_separator(self, parent):
        """Add horizontal separator"""
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 15))
    
    def _collect_widget_references(self):
        """Collect widget references for external access"""
        return {
            'btn_load': self.btn_load,
            'lbl_file': self.lbl_file,
            'lbl_marker_coords': self.lbl_marker_coords,
            'land_unit': self.land_unit,
            'width_label': self.width_label,
            'height_label': self.height_label,
            'entry_land_width': self.entry_land_width,
            'entry_land_height': self.entry_land_height,
            'entry_obj_width': self.entry_obj_width,
            'entry_obj_height': self.entry_obj_height,
            'pack_mode': self.pack_mode,
            'entry_num_objects': self.entry_num_objects,
            'entry_panel_efficiency': self.entry_panel_efficiency,
            'entry_perf_ratio': self.entry_perf_ratio,
            'btn_run_packing': self.btn_run_packing,
            'lbl_panels_packed': self.lbl_panels_packed,
            'lbl_annual_energy': self.lbl_annual_energy,
            'lbl_additional_stats': self.lbl_additional_stats
        }