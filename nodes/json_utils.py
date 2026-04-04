"""
APZmedia JSON Utility Nodes
Additional JSON processing and manipulation utilities
"""

import json
import re
from typing import Any, Dict, List, Optional, Union

from .utils import get_value_type


class APZmediaJSONValidator:
    """Validate and format JSON strings"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_input": ("STRING", {"default": "{}", "multiline": True}),
                "format_output": ("BOOLEAN", {"default": True}),
                "indent_size": ("INT", {"default": 2, "min": 0, "max": 8, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "BOOLEAN")
    RETURN_NAMES = ("formatted_json", "error_message", "is_valid")
    FUNCTION = "validate_and_format"
    CATEGORY = "APZmedia/JSON Utils"

    def validate_and_format(self, json_input: str, format_output: bool = True, indent_size: int = 2) -> tuple:
        try:
            data = json.loads(json_input)

            if format_output:
                formatted = json.dumps(data, indent=indent_size, ensure_ascii=False, sort_keys=True)
            else:
                formatted = json.dumps(data, ensure_ascii=False)

            return formatted, "", True

        except json.JSONDecodeError as e:
            return json_input, f"Invalid JSON: {str(e)}", False
        except Exception as e:
            return json_input, f"Error: {str(e)}", False


class APZmediaJSONMerger:
    """Merge multiple JSON objects"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_1": ("STRING", {"default": "{}", "multiline": True}),
                "json_2": ("STRING", {"default": "{}", "multiline": True}),
                "merge_strategy": (["replace", "combine", "deep_merge"], {"default": "replace"}),
            },
            "optional": {
                "json_3": ("STRING", {"default": "{}", "multiline": True}),
                "json_4": ("STRING", {"default": "{}", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("merged_json", "error_message")
    FUNCTION = "merge_jsons"
    CATEGORY = "APZmedia/JSON Utils"

    def merge_jsons(self, json_1: str, json_2: str, merge_strategy: str = "replace",
                    json_3: str = "{}", json_4: str = "{}") -> tuple:
        try:
            jsons = [json_1, json_2, json_3, json_4]
            data_objects = []

            for json_str in jsons:
                if json_str.strip():
                    data_objects.append(json.loads(json_str))

            if not data_objects:
                return "{}", ""

            result = data_objects[0].copy() if isinstance(data_objects[0], dict) else data_objects[0]

            for data in data_objects[1:]:
                if merge_strategy == "replace":
                    if isinstance(result, dict) and isinstance(data, dict):
                        result.update(data)
                    else:
                        result = data
                elif merge_strategy == "combine":
                    if isinstance(result, list) and isinstance(data, list):
                        result = result + data
                    elif isinstance(result, dict) and isinstance(data, dict):
                        # Extend list values under matching keys; otherwise overwrite
                        for key, value in data.items():
                            if key in result and isinstance(result[key], list) and isinstance(value, list):
                                result[key] = result[key] + value
                            else:
                                result[key] = value
                    else:
                        result = data
                elif merge_strategy == "deep_merge":
                    result = self._deep_merge(result, data)

            merged_json = json.dumps(result, indent=2, ensure_ascii=False)
            return merged_json, ""

        except json.JSONDecodeError as e:
            return "{}", f"Invalid JSON: {str(e)}"
        except Exception as e:
            return "{}", f"Error: {str(e)}"

    def _deep_merge(self, dict1: Dict, dict2: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = dict1.copy()

        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result


class APZmediaJSONPathExtractor:
    """Extract values using JSONPath expressions"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_input": ("STRING", {"default": "{}", "multiline": True}),
                "json_path": ("STRING", {"default": "$.key", "tooltip": "JSONPath expression (e.g., $.user.name, $[*].id)"}),
                "default_value": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("extracted_value", "value_type", "error_message")
    FUNCTION = "extract_with_jsonpath"
    CATEGORY = "APZmedia/JSON Utils"

    def extract_with_jsonpath(self, json_input: str, json_path: str, default_value: str = "") -> tuple:
        try:
            data = json.loads(json_input)

            if json_path.startswith("$."):
                path_parts = json_path[2:].split(".")
                value = self._get_nested_value(data, path_parts)
            elif re.match(r'^\$\[\*\]', json_path):
                value = self._get_array_values(data, json_path)
            else:
                value = data.get(json_path, default_value) if isinstance(data, dict) else default_value

            if value is None:
                extracted_value = default_value
            elif isinstance(value, (dict, list)):
                extracted_value = json.dumps(value, indent=2)
            else:
                extracted_value = str(value)

            return extracted_value, get_value_type(value), ""

        except json.JSONDecodeError as e:
            return default_value, "string", f"Invalid JSON: {str(e)}"
        except Exception as e:
            return default_value, "string", f"Error: {str(e)}"

    def _get_nested_value(self, data: Any, path_parts: List[str]) -> Any:
        """Get nested value using path parts"""
        current = data

        for part in path_parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def _get_array_values(self, data: Any, json_path: str) -> List[Any]:
        """Get values from array using JSONPath.

        Supports:
          $[*]         — return all items in the root array
          $[*].key     — return 'key' from each item in the root array
        """
        key_match = re.match(r'^\$\[\*\]\.(.+)$', json_path)

        if key_match:
            key = key_match.group(1)
            if isinstance(data, list):
                return [item[key] for item in data if isinstance(item, dict) and key in item]
            elif isinstance(data, dict):
                results = []
                for value in data.values():
                    if isinstance(value, list):
                        results.extend(item[key] for item in value if isinstance(item, dict) and key in item)
                return results
            return []
        else:
            # $[*] with no property — return items as-is
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                results = []
                for value in data.values():
                    if isinstance(value, list):
                        results.extend(value)
                return results
            return []


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "APZmediaJSONValidator": APZmediaJSONValidator,
    "APZmediaJSONMerger": APZmediaJSONMerger,
    "APZmediaJSONPathExtractor": APZmediaJSONPathExtractor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APZmediaJSONValidator": "APZmedia JSON Validator",
    "APZmediaJSONMerger": "APZmedia JSON Merger",
    "APZmediaJSONPathExtractor": "APZmedia JSON Path Extractor",
}
