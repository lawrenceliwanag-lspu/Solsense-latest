"""
Input validation helpers
"""
import re

class InputValidator:
    def __init__(self):
        pass
    
    def validate_positive_float(self, value_str, field_name):
        """
        Validate that input is a positive float
        
        Returns:
            tuple: (is_valid, error_message, parsed_value)
        """
        try:
            value = float(value_str)
            if value <= 0:
                return False, f"{field_name} must be positive", None
            return True, "", value
        except ValueError:
            return False, f"{field_name} must be a valid number", None
    
    def validate_positive_integer(self, value_str, field_name):
        """Validate that input is a positive integer"""
        try:
            value = int(value_str)
            if value <= 0:
                return False, f"{field_name} must be positive", None
            return True, "", value
        except ValueError:
            return False, f"{field_name} must be a valid integer", None
    
    def validate_percentage(self, value_str, field_name):
        """Validate percentage input (0-100)"""
        try:
            value = float(value_str)
            if not (0 < value <= 100):
                return False, f"{field_name} must be between 0 and 100", None
            return True, "", value
        except ValueError:
            return False, f"{field_name} must be a valid number", None
    
    def validate_ratio(self, value_str, field_name):
        """Validate ratio input (0-1)"""
        try:
            value = float(value_str)
            if not (0 < value <= 1):
                return False, f"{field_name} must be between 0 and 1", None
            return True, "", value
        except ValueError:
            return False, f"{field_name} must be a valid number", None
    
    def validate_packing_inputs(self, width_input, height_input, panel_width, panel_height, unit, num_objects=None):
        """Validate all packing-related inputs"""
        errors = []
        
        # Validate land dimensions
        is_valid, error, _ = self.validate_positive_float(width_input, "Land width/area")
        if not is_valid:
            errors.append(error)
        
        if unit == "meters":
            is_valid, error, _ = self.validate_positive_float(height_input, "Land height")
            if not is_valid:
                errors.append(error)
        
        # Validate panel dimensions
        is_valid, error, _ = self.validate_positive_float(panel_width, "Panel width")
        if not is_valid:
            errors.append(error)
            
        is_valid, error, _ = self.validate_positive_float(panel_height, "Panel height")
        if not is_valid:
            errors.append(error)
        
        # Validate number of objects if specified
        if num_objects is not None:
            is_valid, error, _ = self.validate_positive_integer(num_objects, "Number of objects")
            if not is_valid:
                errors.append(error)
        
        return errors
    
    def validate_energy_inputs(self, efficiency, performance_ratio):
        """Validate energy calculation inputs"""
        errors = []
        
        is_valid, error, _ = self.validate_percentage(efficiency, "Panel efficiency")
        if not is_valid:
            errors.append(error)
            
        is_valid, error, _ = self.validate_ratio(performance_ratio, "Performance ratio")
        if not is_valid:
            errors.append(error)
        
        return errors
    
    def sanitize_filename(self, filename):
        """Sanitize filename for safe file operations"""
        # Remove invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip('. ')
        
        # Limit length
        if len(sanitized) > 100:
            name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
            sanitized = name[:95] + ('.' + ext if ext else '')
        
        return sanitized if sanitized else 'untitled'