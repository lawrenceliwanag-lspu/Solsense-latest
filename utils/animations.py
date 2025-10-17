"""
Animation handling for loading and data visualization
"""
import numpy as np
from matplotlib.animation import FuncAnimation
from config.settings import APP_SETTINGS

class AnimationManager:
    def __init__(self, fig, ax, canvas):
        self.fig = fig
        self.ax = ax
        self.canvas = canvas
        self.animation = None
        self.is_animating = False
        self.animation_frame = 0
        self.animation_interval = APP_SETTINGS['animation_interval']
        self.reveal_interval = APP_SETTINGS['data_reveal_interval']
    
    def start_loading_animation(self, colors):
        """Start a rotating loading indicator animation"""
        self.stop_all_animations()
        self.is_animating = True
        self.animation_frame = 0
        
        def animate(frame):
            if not self.is_animating:
                return
            
            self.ax.clear()

            # Create rotating loading indicator
            angles = [i * 45 for i in range(8)]
            alphas = [0.1 + (0.9 * ((frame + i) % 8) / 7) for i in range(8)]
            
            for angle, alpha in zip(angles, alphas):
                x = 0.5 + 0.3 * np.cos(np.radians(angle))
                y = 0.5 + 0.3 * np.sin(np.radians(angle))
                self.ax.plot(x, y, 'o', markersize=10, alpha=alpha, color=colors['primary'])
            
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.set_title("Loading GeoTIFF...")
            self.ax.axis('off')
            
        self.animation = FuncAnimation(
            self.fig, animate, 
            interval=self.animation_interval, 
            repeat=True, 
            cache_frame_data=False
        )
        self.canvas.draw()
    
    def start_data_reveal_animation(self, display_image_rgba, colors):
        """Animate slope data visualization with row-by-row reveal effect"""
        if display_image_rgba is None:
            return
        
        self.stop_all_animations()
        self.animation_frame = 0
        rows, cols = display_image_rgba.shape[:2]
        
        def animate(frame):
            if frame >= rows:
                # Animation complete, stop
                try:
                    self.animation.event_source.stop()
                except:
                    pass
                self.animation = None
                return
            
            self.ax.clear()
            
            # Create mask that reveals data row by row
            mask = np.zeros((rows, cols), dtype=bool)
            mask[:frame+1, :] = True
            
            # Apply mask to display image
            masked_image = display_image_rgba.copy()
            masked_image[~mask] = [50, 50, 50, 255]  # Gray out unrevealed areas
            
            self.ax.imshow(masked_image)
            
            # Add title with legend
            self._add_slope_legend(colors)
            
            self.ax.set_xlabel("Pixel X")
            self.ax.set_ylabel("Pixel Y")
        
        self.animation = FuncAnimation(
            self.fig, animate, 
            frames=rows, 
            interval=self.reveal_interval, 
            repeat=False, 
            cache_frame_data=False
        )
        self.canvas.draw()
    
    def _add_slope_legend(self, colors):
        """Add colored legend to slope visualization"""
        title_y = 1.02
        spacing = 0.12
        
        # Clear any existing title
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
    
    def stop_loading_animation(self):
        """Stop the loading animation"""
        self.is_animating = False
        if self.animation is not None:
            try:
                self.animation.event_source.stop()
            except:
                pass
            self.animation = None
    
    def stop_all_animations(self):
        """Stop all running animations and reset state"""
        self.is_animating = False
        if self.animation is not None:
            try:
                self.animation.event_source.stop()
            except:
                pass
            self.animation = None
        self.animation_frame = 0