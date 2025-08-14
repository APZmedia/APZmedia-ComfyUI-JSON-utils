"""
APZmedia JSON Key Extractor Node
Extracts values from JSON using dynamic key widgets
"""

import json
import re
from typing import Any, Dict, List, Optional, Union


class APZmediaJSONKeyExtractor:
    """Extract values from JSON using dynamic key widgets"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_input": ("STRING", {"default": "{}", "multiline": True}),
                "key_name": ("STRING", {"default": "key"}),
                "default_value": ("STRING", {"default": ""}),
                "nested_key_path": ("STRING", {"default": "", "tooltip": "Use dot notation for nested keys (e.g., 'user.profile.name')"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("extracted_value", "value_type", "error_message")
    FUNCTION = "extract_json_value"
    CATEGORY = "APZmedia/JSON Utils"
    
    def extract_json_value(self, json_input: str, key_name: str, default_value: str, nested_key_path: str = "") -> tuple:
        """
        Extract a value from JSON using the specified key
        
        Args:
            json_input: JSON string to parse
            key_name: Key to extract (widget input)
            default_value: Default value if key doesn't exist
            nested_key_path: Dot-notation path for nested keys
            
        Returns:
            tuple: (extracted_value, value_type, error_message)
        """
        try:
            # Parse JSON input
            if not json_input.strip():
                return default_value, "string", "Empty JSON input"
            
            data = json.loads(json_input)
            
            # Determine the key to use
            target_key = nested_key_path if nested_key_path else key_name
            
            # Extract value using dot notation for nested keys
            if "." in target_key:
                value = self._get_nested_value(data, target_key)
            else:
                value = data.get(target_key, default_value)
            
            # Determine value type
            value_type = self._get_value_type(value)
            
            # Convert value to string for output
            if value is None:
                extracted_value = default_value
            elif isinstance(value, (dict, list)):
                extracted_value = json.dumps(value, indent=2)
            else:
                extracted_value = str(value)
            
            return extracted_value, value_type, ""
            
        except json.JSONDecodeError as e:
            return default_value, "string", f"Invalid JSON: {str(e)}"
        except Exception as e:
            return default_value, "string", f"Error: {str(e)}"
    
    def _get_nested_value(self, data: Any, key_path: str) -> Any:
        """
        Get nested value using dot notation
        
        Args:
            data: JSON data
            key_path: Dot-notation path (e.g., 'user.profile.name')
            
        Returns:
            The value at the specified path
        """
        keys = key_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    def _get_value_type(self, value: Any) -> str:
        """
        Determine the type of a value
        
        Args:
            value: The value to check
            
        Returns:
            String representation of the type
        """
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "unknown"


class APZmediaJSONMultiKeyExtractor:
    """Extract multiple values from JSON using multiple key widgets"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_input": ("STRING", {"default": "{}", "multiline": True}),
                "key_1": ("STRING", {"default": "key1"}),
                "key_2": ("STRING", {"default": "key2"}),
                "key_3": ("STRING", {"default": "key3"}),
                "key_4": ("STRING", {"default": "key4"}),
                "key_5": ("STRING", {"default": "key5"}),
                "default_value": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("value_1", "value_2", "value_3", "value_4", "value_5")
    FUNCTION = "extract_multiple_values"
    CATEGORY = "APZmedia/JSON Utils"
    
    def extract_multiple_values(self, json_input: str, key_1: str, key_2: str, key_3: str, 
                               key_4: str, key_5: str, default_value: str) -> tuple:
        """
        Extract multiple values from JSON using multiple keys
        
        Args:
            json_input: JSON string to parse
            key_1-5: Keys to extract
            default_value: Default value if key doesn't exist
            
        Returns:
            tuple: (value_1, value_2, value_3, value_4, value_5)
        """
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError:
            return (default_value, default_value, default_value, default_value, default_value)
        
        keys = [key_1, key_2, key_3, key_4, key_5]
        values = []
        
        for key in keys:
            if key.strip():
                value = data.get(key, default_value)
                if isinstance(value, (dict, list)):
                    values.append(json.dumps(value, indent=2))
                else:
                    values.append(str(value))
            else:
                values.append(default_value)
        
        return tuple(values)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "APZmediaJSONKeyExtractor": APZmediaJSONKeyExtractor,
    "APZmediaJSONMultiKeyExtractor": APZmediaJSONMultiKeyExtractor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APZmediaJSONKeyExtractor": "APZmedia JSON Key Extractor",
    "APZmediaJSONMultiKeyExtractor": "APZmedia JSON Multi-Key Extractor",
} 