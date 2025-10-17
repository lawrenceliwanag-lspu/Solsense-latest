"""
Application styling and theme configuration
"""
from tkinter import ttk
from config.settings import COLORS

class AppStyles:
    def __init__(self):
        self.colors = COLORS
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()

        # Configure notebook style for tabs
        style.configure('Modern.TNotebook',
                       background=self.colors['surface'],
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       background=self.colors['background'],
                       foreground=self.colors['text_primary'],
                       padding=[20, 10],
                       focuscolor='none')
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                            ('active', self.colors['primary_dark'])],
                 foreground=[('selected', 'white'),
                            ('active', 'white')])

        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=[20, 10])
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_dark']),
                            ('pressed', self.colors['primary_dark'])])

        style.configure('Secondary.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=[15, 8])
        style.map('Secondary.TButton',
                 background=[('active', '#F57C00'),
                            ('pressed', '#F57C00')])

        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=1)

        # Configure labelframe styles
        style.configure('Modern.TLabelframe',
                       background=self.colors['surface'],
                       borderwidth=2,
                       relief='flat')
        style.configure('Modern.TLabelframe.Label',
                       background=self.colors['surface'],
                       foreground=self.colors['primary'],
                       font=('Segoe UI', 10, 'bold'))

        # Configure entry styles
        style.configure('Modern.TEntry',
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid',
                       padding=[10, 8])
        style.map('Modern.TEntry',
                 fieldbackground=[('readonly', '#f5f5f5')],
                 foreground=[('disabled', '#9e9e9e')],
                 bordercolor=[('focus', self.colors['primary'])])