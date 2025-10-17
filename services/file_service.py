"""
File operations and validation services
"""
import os
from tkinter import filedialog, messagebox

class FileService:
    def __init__(self):
        self.supported_extensions = ('.tif', '.tiff')
    
    def select_geotiff_file(self):
        """Open file dialog to select GeoTIFF file"""
        filepath = filedialog.askopenfilename(
            title="Select GeoTIFF File",
            filetypes=[
                ("GeoTIFF files", "*.tif *.tiff"), 
                ("All files", "*.*")
            ]
        )
        return filepath if filepath else None
    
    def validate_file_exists(self, filepath):
        """Check if file exists and is accessible"""
        if not filepath:
            return False, "No file path provided"
        
        if not os.path.exists(filepath):
            return False, f"File does not exist: {filepath}"
        
        if not os.path.isfile(filepath):
            return False, f"Path is not a file: {filepath}"
        
        if not os.access(filepath, os.R_OK):
            return False, f"File is not readable: {filepath}"
        
        return True, "File is valid"
    
    def validate_geotiff_extension(self, filepath):
        """Check if file has valid GeoTIFF extension"""
        if not filepath:
            return False, "No file path provided"
        
        _, ext = os.path.splitext(filepath.lower())
        if ext not in self.supported_extensions:
            return False, f"Unsupported file extension: {ext}. Expected: {', '.join(self.supported_extensions)}"
        
        return True, "Valid GeoTIFF extension"
    
    def get_file_info(self, filepath):
        """Get basic file information"""
        try:
            stat = os.stat(filepath)
            filename = os.path.basename(filepath)
            size_mb = stat.st_size / (1024 * 1024)
            
            return {
                'filename': filename,
                'size_mb': round(size_mb, 2),
                'full_path': filepath
            }
        except Exception as e:
            return None
    
    def show_file_error(self, message):
        """Display file-related error message"""
        messagebox.showerror("File Error", message)
    
    def show_file_warning(self, message):
        """Display file-related warning message"""
        messagebox.showwarning("File Warning", message)