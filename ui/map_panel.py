"""
Map display area with matplotlib integration
"""
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.patheffects as PathEffects
from PIL import Image, ImageTk
from config.settings import COLORS, RESOURCE_PATHS

class MapPanel:
    def __init__(self, parent_frame, app_callbacks):
        self.parent_frame = parent_frame
        self.callbacks = app_callbacks
        self.colors = COLORS
        
        # Create scrollable map container
        self._create_scrollable_container()
        
        # Create map components
        self._create_map_container()
        self._create_matplotlib_components()
        self._create_toolbar()
        self._setup_map_interactions()

        
        # Initialize map styling
        self._style_matplotlib_figure()
    
    def _create_scrollable_container(self):
        """Create scrollable container for map content"""
        map_canvas = tk.Canvas(self.parent_frame, bg=self.colors['surface'], highlightthickness=0)
        map_scrollbar_v = tk.Scrollbar(self.parent_frame, orient="vertical", command=map_canvas.yview)
        
        # Scrollable frame inside canvas
        self.scrollable_map_frame = tk.Frame(map_canvas, bg=self.colors['surface'])
        
        # Configure scrolling
        self.scrollable_map_frame.bind(
            "<Configure>",
            lambda e: map_canvas.configure(scrollregion=map_canvas.bbox("all"))
        )
        
        map_canvas.create_window((0, 0), window=self.scrollable_map_frame, anchor="nw")
        map_canvas.configure(yscrollcommand=map_scrollbar_v.set)
        
        # Pack scrollbars and canvas
        map_scrollbar_v.pack(side="right", fill="y")
        map_canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            map_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        map_canvas.bind("<MouseWheel>", _on_mousewheel)  # Windows
        map_canvas.bind("<Button-4>", lambda e: map_canvas.yview_scroll(-1, "units"))  # Linux
        map_canvas.bind("<Button-5>", lambda e: map_canvas.yview_scroll(1, "units"))   # Linux
    
    def _create_map_container(self):
        """Create map container with background overlay"""
        self.map_container = tk.Frame(
            self.scrollable_map_frame, 
            bg=self.colors['surface'],
            relief=tk.FLAT, 
            borderwidth=2,
            width=1500, height=1080
        )
        self.map_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, anchor='e')
        self.map_container.pack_propagate(False)
        # Map title
        map_title = tk.Label(
            self.map_container,
            text="🗺️ Geographic Analysis View",
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 12, 'bold')
        )
        map_title.pack(pady=(10, 5))
    
    def _create_matplotlib_components(self):
        """Create matplotlib figure and canvas"""
        self.fig = Figure(figsize=(10, 8), facecolor=self.colors['surface'])
        self.fig.patch.set_facecolor(self.colors['surface'])
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.map_container)
        self.canvas_widget = self.canvas.get_tk_widget()
    
    def _create_toolbar(self):
        """Create matplotlib navigation toolbar"""
        # Pack canvas widget first (at the top)
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Then create toolbar frame below the canvas
        toolbar_frame = tk.Frame(self.map_container, bg=self.colors['surface'])
        toolbar_frame.pack(fill=tk.X, padx=10, pady=(0, 5))

        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=tk.LEFT)
    
    def _setup_map_interactions(self):
        """Setup map click interactions"""
        self.fig.canvas.mpl_connect('button_press_event', self.callbacks['map_click'])
    
    def _style_matplotlib_figure(self):
        """Apply styling to matplotlib components"""
        self.ax.set_facecolor('#fafafa')
        self.ax.grid(True, alpha=0.3)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_color('#e0e0e0')
        self.ax.spines['left'].set_color('#e0e0e0')

        # Set axis label and tick colors
        self.ax.xaxis.label.set_color(self.colors['text_primary'])
        self.ax.yaxis.label.set_color(self.colors['text_primary'])
        self.ax.tick_params(axis='x', colors=self.colors['text_primary'])
        self.ax.tick_params(axis='y', colors=self.colors['text_primary'])
    
    def _add_image_overlay(self, target_frame, image_path, store_as_attribute_name):
        """Add background image overlay to frame"""
        try:
            # Force frame to update its size
            target_frame.update_idletasks()
            
            # Get frame dimensions (use default if not rendered yet)
            frame_width = 1920
            frame_height = 1080
            
            # Load and resize image
            overlay_image = Image.open(image_path)
            overlay_image = overlay_image.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
            
            # Convert to tkinter format and store reference
            photo = ImageTk.PhotoImage(overlay_image)
            setattr(self, store_as_attribute_name, photo)
            
            # Create overlay label
            overlay_label = tk.Label(target_frame, 
                                image=photo,
                                bg=target_frame.cget('bg'))
            
            # Place overlay
            overlay_label.place(x=0, y=0, relwidth=1, relheight=1)
            overlay_label.lower()
            
            return overlay_label
            
        except Exception as e:
            print(f"Could not add overlay to frame: {e}")
            return None
    
    def display_slope_data(self, display_image_rgba):
        """Display slope visualization on map"""
        if display_image_rgba is None:
            self.ax.text(0.5, 0.5, "No valid slope data to display.", 
                        ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return
        
        self.ax.clear()
        self.ax.imshow(display_image_rgba)
        
        # Add legend
        self._add_slope_legend()
        
        self.ax.set_xlabel("Pixel X")
        self.ax.set_ylabel("Pixel Y")
        self.canvas.draw()
    
    def _add_slope_legend(self):
        """Add colored legend to slope visualization"""
        title_y = 1.02
        spacing = 0.12
        
        self.ax.set_title("")

        self.ax.text(0.1 + spacing, title_y, "■ ", transform=self.ax.transAxes,
                    color='#00AA00', fontsize=12, fontweight='normal')
        self.ax.text(0.1 + spacing*1.5, title_y, "<5° + South", transform=self.ax.transAxes,
                    color='black', fontsize=10, fontweight='bold')

        self.ax.text(0.1 + spacing*3.5, title_y, "■ ", transform=self.ax.transAxes,
                    color='#CCCC00', fontsize=12, fontweight='normal')
        self.ax.text(0.1 + spacing*4, title_y, "<5° other", transform=self.ax.transAxes,
                    color='black', fontsize=10, fontweight='bold')

        self.ax.text(0.1 + spacing*5.5, title_y, "■ ", transform=self.ax.transAxes,
                    color='#808080', fontsize=12, fontweight='normal')
        self.ax.text(0.1 + spacing*6, title_y, "≥5°", transform=self.ax.transAxes,
                    color='black', fontsize=10, fontweight='bold')
    
    def draw_marker(self, pixel_coords):
        """Draw marker on map at specified pixel coordinates"""
        if pixel_coords and self.ax:
            col, row = pixel_coords
            marker = self.ax.plot(col, row, 'ro', markersize=8, markeredgecolor='white',
                                 path_effects=[PathEffects.withStroke(linewidth=2, foreground='black')])
            self.canvas.draw_idle()
            return marker
        return None
    
    def clear_marker(self, marker_object):
        """Remove marker from map"""
        if marker_object:
            try:
                if isinstance(marker_object, list):
                    for m in marker_object:
                        m.remove()
                else:
                    marker_object.remove()
                self.canvas.draw_idle()
            except:
                pass
    
    def clear_display(self):
        """Clear the map display"""
        self.ax.clear()
        self._style_matplotlib_figure()
        self.canvas.draw()
    
    def redraw(self):
        """Force canvas redraw"""
        self.canvas.draw_idle()