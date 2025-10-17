"""
Tutorial popup dialog for GeoTIFF data acquisition
"""
import tkinter as tk
from tkinter import ttk
import webbrowser
from config.settings import COLORS

class TutorialDialog:
    def __init__(self, parent):
        self.parent = parent
        self.colors = COLORS
        self.popup = None
    
    def show_tutorial(self):
        """Display tutorial popup window"""
        # Create popup window
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("GeoTIFF Tutorial")
        self.popup.geometry("700x600")
        self.popup.configure(bg='white')
        self.popup.resizable(True, True)
        
        # Make it modal
        self.popup.transient(self.parent)
        self.popup.grab_set()
        
        # Center popup
        self._center_popup()
        
        # Create content
        self._create_header()
        self._create_scrollable_content()
        self._create_button_frame()
        
        # Focus on popup
        self.popup.focus_set()
    
    def _center_popup(self):
        """Center popup relative to parent window"""
        self.parent.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 350
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 300
        self.popup.geometry(f"700x600+{x}+{y}")
    
    def _create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.popup, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_title = tk.Label(
            header_frame,
            text="How to Download NASADEM Data from OpenTopography",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        header_title.pack(expand=True)
    
    def _create_scrollable_content(self):
        """Create scrollable content area"""
        content_frame = tk.Frame(self.popup, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Scrollable text area
        canvas = tk.Canvas(content_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add tutorial content
        self._add_tutorial_content(scrollable_frame)
        
        # Pack scrollbar and canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
    
    def _add_tutorial_content(self, parent):
        """Add tutorial steps content"""
        # Introduction
        intro_text = tk.Label(
            parent,
            text="This tutorial will guide you through downloading NASADEM (NASA Digital Elevation Model) data from OpenTopography.",
            font=('Segoe UI', 10),
            fg='#333333',
            bg='white',
            justify='left',
            wraplength=650
        )
        intro_text.pack(anchor='w', pady=(0, 20))
        
        # Step 1
        self._add_step(parent, 1, "Navigate to the Data Map",
            "1. Go to the OpenTopography website.\n"
            "2. In the main menu, hover over Data and then click on Find Data Map."
        )
        
        # Step 2
        self._add_step(parent, 2, "Select Your Region of Interest",
            "1. Use the map to find your location. Pan by clicking and dragging, zoom with scroll wheel or +/- buttons.\n"
            "2. Click the 'Select a Region' button at the top left corner of the map.\n"
            "3. Click and drag on the map to draw a box around your desired area."
        )
        
        # Step 3
        self._add_step(parent, 3, "Choose the NASADEM Dataset",
            "1. After selecting your region, available datasets will appear at the bottom.\n"
            "2. Scroll through the list to find NASADEM.\n"
            "3. Click on the 'Get NASADEM data' button."
        )
        
        # Step 4
        self._add_step(parent, 4, "Submit Your Data Request",
            "1. You'll be taken to a page with NASADEM dataset details.\n"
            "2. Scroll down to the bottom of the page.\n"
            "3. Enter your email address in the provided field.\n"
            "4. Click the Submit button."
        )
        
        # Step 5
        self._add_step(parent, 5, "Download Your Data",
            "1. You'll receive an email when your data is ready (may take a few minutes).\n"
            "2. Open the email and click on the download link.\n"
            "3. Look for a file named 'rasters_NASADEM.tar.gz' and download it."
        )
        
        # OpenTopography link
        link_frame = tk.Frame(parent, bg='white')
        link_frame.pack(anchor='w', fill='x', pady=(20, 15))
        
        tk.Label(link_frame, text="OpenTopography website: ", 
                font=('Segoe UI', 10), fg='#333333', bg='white').pack(side='left')
        
        opentopo_link = tk.Label(link_frame, text="https://opentopography.org", 
                                font=('Segoe UI', 10, 'underline'), fg='#2196F3', 
                                bg='white', cursor='hand2')
        opentopo_link.pack(side='left')
        opentopo_link.bind('<Button-1>', lambda e: self._open_url('https://opentopography.org'))
    
    def _add_step(self, parent, step_num, title, content):
        """Add a tutorial step"""
        # Step title
        step_title = tk.Label(
            parent,
            text=f"Step {step_num}: {title}",
            font=('Segoe UI', 12, 'bold'),
            fg='#2196F3',
            bg='white'
        )
        step_title.pack(anchor='w', pady=(0, 10))
        
        # Step content
        step_text = tk.Label(
            parent,
            text=content,
            font=('Segoe UI', 10),
            fg='#333333',
            bg='white',
            justify='left',
            wraplength=650
        )
        step_text.pack(anchor='w', pady=(0, 15))
    
    def _create_button_frame(self):
        """Create button frame with close button"""
        button_frame = tk.Frame(self.popup, bg='white')
        button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        close_btn = ttk.Button(
            button_frame,
            text="Close",
            command=self.popup.destroy
        )
        close_btn.pack(side='right')
    
    def _open_url(self, url):
        """Open URL in default browser"""
        webbrowser.open(url)