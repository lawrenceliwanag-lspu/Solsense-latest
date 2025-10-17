"""
Splash screen component
"""
import tkinter as tk
from PIL import Image, ImageTk
from config.settings import RESOURCE_PATHS

class SplashScreen:
    def __init__(self):
        self.splash = tk.Tk()
        self.splash.title("SolSense")
        self.splash.overrideredirect(True)  # Remove window decorations
        
        # Get screen dimensions and center splash screen
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        splash_width = 500
        splash_height = 350
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        self.splash.configure(bg='black')  # Set a default background
        
        # Try to load and display background image
        try:
            bg_image = Image.open(RESOURCE_PATHS['splash_image'])
            bg_image = bg_image.resize((splash_width, splash_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            # Create background label with image
            self.bg_label = tk.Label(self.splash, image=self.bg_photo, bd=0)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        except Exception as e:
            # Fallback if image can't be loaded
            print(f"Could not load splash image: {e}")
            self.splash.configure(bg='#1d2427')
        
        self.status_label = tk.Label(self.splash, text="Initializing...",
                                   font=('Segoe UI', 12, 'bold'),
                                   fg='white', bg='#1d2427', bd=0, highlightthickness=0)
        self.status_label.place(relx=0.5, rely=0.85, anchor='center')
        
        # Add shadow for status text
        self.status_shadow = tk.Label(self.splash, text="Initializing...",
                                     font=('Segoe UI', 12, 'bold'),
                                     fg="#FFFFFF", bg='#1d2427', bd=0, highlightthickness=0)
        self.status_shadow.place(relx=0.502, rely=0.852, anchor='center')
        
        # Center splash on screen
        self.splash.update_idletasks()
        self.splash.lift()
        self.splash.attributes('-topmost', True)
        
    def update_status(self, text):
        self.status_label.config(text=text)
        self.status_shadow.config(text=text)  # Update shadow too
        self.splash.update_idletasks()
        
    def close(self):
        self.splash.destroy()