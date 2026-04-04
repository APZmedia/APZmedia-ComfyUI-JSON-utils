"""
APZmedia CSV Reader Node
Reads CSV files and provides dynamic outputs for each column
"""

import os
import pandas as pd
import json
from typing import Any, Dict, List, Optional, Tuple, Union


class APZmediaDynamicCSVReader:
    """CSV Reader that adapts to any CSV structure; column data is accessible via csv_data_json"""

    def __init__(self):
        self.df = None
        self.column_names = []
        self.row_count = 0
        self.current_row = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": "/path/to/your/file.csv", "tooltip": "Path to the CSV file (e.g., /Users/username/Documents/data.csv)"}),
                "selected_row": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1, "tooltip": "Row index to extract (0-based)"}),
                "delimiter": ("STRING", {"default": ",", "tooltip": "CSV delimiter character"}),
                "encoding": ("STRING", {"default": "utf-8", "tooltip": "File encoding"}),
            },
            "optional": {
                "refresh_trigger": ("STRING", {"default": "", "tooltip": "Internal trigger for button updates"}),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("column_names", "row_count", "csv_info", "error_message", "csv_data_json")

    FUNCTION = "read_csv_dynamic"
    CATEGORY = "APZmedia/CSV Utils"

    def read_csv_dynamic(self, csv_path: str, selected_row: int, delimiter: str = ",",
                         encoding: str = "utf-8", refresh_trigger: str = "") -> tuple:
        try:
            if not csv_path:
                return ("No file", 0, "File not found", "No file path provided", "{}")

            csv_path = os.path.normpath(csv_path.strip())

            if not os.path.exists(csv_path):
                return ("No file", 0, "File not found", f"File not found: {csv_path}", "{}")

            should_reload = (
                self.df is None or
                not hasattr(self, '_last_csv_path') or
                self._last_csv_path != csv_path or
                refresh_trigger != getattr(self, '_last_refresh_trigger', "")
            )

            if should_reload:
                self.df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
                self.column_names = self.df.columns.tolist()
                self.row_count = len(self.df)
                self._last_csv_path = csv_path
                self._last_refresh_trigger = refresh_trigger
                print(f"CSV loaded: {len(self.column_names)} columns, {self.row_count} rows")
                print(f"Columns: {', '.join(self.column_names)}")
                if refresh_trigger:
                    print("CSV reloaded via button click - structure updated!")

            if selected_row < 0:
                selected_row = 0
            if selected_row >= self.row_count:
                selected_row = 0
            self.current_row = selected_row

            column_names_str = ", ".join(self.column_names)
            csv_info = f"File: {os.path.basename(csv_path)} | Rows: {self.row_count} | Columns: {len(self.column_names)} | Selected Row: {selected_row}"

            row_dict = self.df.iloc[selected_row].to_dict()
            row_data_json = json.dumps(row_dict, indent=2, ensure_ascii=False)

            return (column_names_str, self.row_count, csv_info, "", row_data_json)

        except Exception as e:
            print(f"Error in CSV reader: {e}")
            return ("Error", 0, "Error occurred", str(e), "{}")


class APZmediaCSVReader:
    """CSV Reader with fixed outputs for maximum compatibility"""

    def __init__(self):
        self.df = None
        self.column_names = []
        self.row_count = 0
        self.current_row = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": "/path/to/your/file.csv", "tooltip": "Path to the CSV file (e.g., /Users/username/Documents/data.csv)"}),
                "selected_row": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1, "tooltip": "Row index to extract (0-based)"}),
                "delimiter": ("STRING", {"default": ",", "tooltip": "CSV delimiter character"}),
                "encoding": ("STRING", {"default": "utf-8", "tooltip": "File encoding"}),
            },
            "optional": {
                "refresh_trigger": ("STRING", {"default": "", "tooltip": "Internal trigger for button updates"}),
            }
        }

    # Fixed outputs with descriptive names based on CSV column positions
    RETURN_TYPES = ("STRING", "INT", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("column_names", "row_count", "csv_info", "error_message", "csv_data_json", "col_1", "col_2", "col_3", "col_4", "col_5", "col_6", "col_7", "col_8", "col_9", "col_10", "col_11", "col_12", "col_13", "col_14", "col_15", "col_16", "col_17", "col_18", "col_19", "col_20", "col_21", "col_22", "col_23", "col_24", "col_25")

    FUNCTION = "read_csv_fixed"
    CATEGORY = "APZmedia/CSV Utils"

    def read_csv_fixed(self, csv_path: str, selected_row: int, delimiter: str = ",",
                       encoding: str = "utf-8", refresh_trigger: str = "") -> tuple:
        try:
            if not csv_path:
                error_outputs = ["No file", 0, "File not found", "No file path provided", "{}"] + [""] * 25
                return tuple(error_outputs)

            csv_path = os.path.normpath(csv_path.strip())

            if not os.path.exists(csv_path):
                error_outputs = ["No file", 0, "File not found", f"File not found: {csv_path}", "{}"] + [""] * 25
                return tuple(error_outputs)

            should_reload = (
                self.df is None or
                not hasattr(self, '_last_csv_path') or
                self._last_csv_path != csv_path or
                refresh_trigger != getattr(self, '_last_refresh_trigger', "")
            )

            if should_reload:
                self.df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
                self.column_names = self.df.columns.tolist()
                self.row_count = len(self.df)
                self._last_csv_path = csv_path
                self._last_refresh_trigger = refresh_trigger
                print(f"CSV loaded: {len(self.column_names)} columns, {self.row_count} rows")
                print(f"Columns: {', '.join(self.column_names)}")
                if refresh_trigger:
                    print("CSV reloaded via button click")

            if selected_row < 0:
                selected_row = 0
            if selected_row >= self.row_count:
                selected_row = 0
            self.current_row = selected_row

            column_names_str = ", ".join(self.column_names)
            csv_info = f"File: {os.path.basename(csv_path)} | Rows: {self.row_count} | Columns: {len(self.column_names)} | Selected Row: {selected_row}"

            row_dict = self.df.iloc[selected_row].to_dict()
            row_data_json = json.dumps(row_dict, indent=2, ensure_ascii=False)

            outputs = [column_names_str, self.row_count, csv_info, "", row_data_json]

            for i in range(25):
                if i < len(self.column_names):
                    value = self.df.iloc[selected_row][self.column_names[i]]
                    outputs.append("" if pd.isna(value) else str(value))
                else:
                    outputs.append("")

            return tuple(outputs)

        except Exception as e:
            error_outputs = ["Error", 0, "Error occurred", str(e), "{}"] + [""] * 25
            return tuple(error_outputs)


class APZmediaCSVColumnExtractor:
    """Extract specific columns by name from CSV"""

    def __init__(self):
        self.df = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": "", "tooltip": "Path to the CSV file"}),
                "selected_row": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "column_names": ("STRING", {"default": "Prompt,Neg-Prompt", "tooltip": "Comma-separated column names to extract"}),
                "delimiter": ("STRING", {"default": ",", "tooltip": "CSV delimiter character"}),
                "encoding": ("STRING", {"default": "utf-8", "tooltip": "File encoding"}),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("column_names", "row_count", "csv_info", "error_message", "col_1", "col_2", "col_3")
    FUNCTION = "extract_columns"
    CATEGORY = "APZmedia/CSV Utils"

    def extract_columns(self, csv_path: str, selected_row: int, column_names: str,
                        delimiter: str = ",", encoding: str = "utf-8") -> tuple:
        try:
            if not csv_path:
                return "No file", 0, "File not found", "No file path provided", "", "", ""

            csv_path = os.path.normpath(csv_path.strip())

            if not os.path.exists(csv_path):
                return "No file", 0, "File not found", f"File not found: {csv_path}", "", "", ""

            should_reload = (
                self.df is None or
                not hasattr(self, '_last_csv_path') or
                self._last_csv_path != csv_path or
                getattr(self, '_last_delimiter', None) != delimiter or
                getattr(self, '_last_encoding', None) != encoding
            )

            if should_reload:
                self.df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
                self._last_csv_path = csv_path
                self._last_delimiter = delimiter
                self._last_encoding = encoding

            all_column_names = ", ".join(self.df.columns.tolist())
            row_count = len(self.df)

            requested_cols = [col.strip() for col in column_names.split(",")]

            if selected_row < 0:
                selected_row = 0
            if selected_row >= row_count:
                selected_row = 0

            csv_info = f"File: {os.path.basename(csv_path)} | Rows: {row_count} | Columns: {len(self.df.columns)} | Selected Row: {selected_row}"

            extracted_values = []
            for col_name in requested_cols[:3]:
                if col_name in self.df.columns:
                    value = self.df.iloc[selected_row][col_name]
                    extracted_values.append("" if pd.isna(value) else str(value))
                else:
                    extracted_values.append(f"(Column '{col_name}' not found)")

            while len(extracted_values) < 3:
                extracted_values.append("")

            return all_column_names, row_count, csv_info, "", *extracted_values

        except Exception as e:
            return "Error", 0, "Error occurred", str(e), "", "", ""


class APZmediaCSVReaderAdvanced:
    """Advanced CSV reader with more flexible column handling"""

    def __init__(self):
        self.df = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": "", "tooltip": "Path to the CSV file"}),
                "selected_row": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "column_indices": ("STRING", {"default": "0,1,2", "tooltip": "Comma-separated column indices to extract"}),
                "delimiter": ("STRING", {"default": ",", "tooltip": "CSV delimiter character"}),
                "encoding": ("STRING", {"default": "utf-8", "tooltip": "File encoding"}),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("column_names", "row_count", "selected_columns", "row_data", "csv_info", "error_message", "status")
    FUNCTION = "read_csv_advanced"
    CATEGORY = "APZmedia/CSV Utils"

    def read_csv_advanced(self, csv_path: str, selected_row: int, column_indices: str,
                          delimiter: str = ",", encoding: str = "utf-8") -> tuple:
        try:
            if not csv_path:
                return "No file", 0, "", "", "", "No file path provided", "error"

            csv_path = os.path.normpath(csv_path.strip())

            if not os.path.exists(csv_path):
                return "No file", 0, "", "", "", f"File not found: {csv_path}", "error"

            should_reload = (
                self.df is None or
                not hasattr(self, '_last_csv_path') or
                self._last_csv_path != csv_path or
                getattr(self, '_last_delimiter', None) != delimiter or
                getattr(self, '_last_encoding', None) != encoding
            )

            if should_reload:
                self.df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
                self._last_csv_path = csv_path
                self._last_delimiter = delimiter
                self._last_encoding = encoding

            column_names = ", ".join(self.df.columns.tolist())
            row_count = len(self.df)

            try:
                indices = [int(idx.strip()) for idx in column_indices.split(",") if idx.strip()]
            except ValueError:
                indices = [0, 1, 2]

            if selected_row < 0:
                selected_row = 0
            if selected_row >= row_count:
                selected_row = 0

            selected_cols = []
            row_data_parts = []

            for idx in indices:
                if 0 <= idx < len(self.df.columns):
                    col_name = self.df.columns[idx]
                    selected_cols.append(col_name)
                    value = self.df.iloc[selected_row, idx]
                    row_data_parts.append("" if pd.isna(value) else str(value))
                else:
                    selected_cols.append(f"col_{idx}")
                    row_data_parts.append("")

            selected_columns = ", ".join(selected_cols)
            row_data = " | ".join(row_data_parts)

            csv_info = f"File: {os.path.basename(csv_path)} | Rows: {row_count} | Columns: {len(self.df.columns)} | Selected Row: {selected_row}"

            return column_names, row_count, selected_columns, row_data, csv_info, "", "success"

        except Exception as e:
            return "Error", 0, "", "", "", str(e), "error"


class APZmediaCSVToJSON:
    """Convert CSV data to JSON format"""

    def __init__(self):
        self.df = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": "", "tooltip": "Path to the CSV file"}),
                "selected_row": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "delimiter": ("STRING", {"default": ",", "tooltip": "CSV delimiter character"}),
                "encoding": ("STRING", {"default": "utf-8", "tooltip": "File encoding"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("json_output", "error_message", "row_count")
    FUNCTION = "csv_to_json"
    CATEGORY = "APZmedia/CSV Utils"

    def csv_to_json(self, csv_path: str, selected_row: int, delimiter: str = ",",
                    encoding: str = "utf-8") -> tuple:
        try:
            if not csv_path:
                return "{}", "No file path provided", 0

            csv_path = os.path.normpath(csv_path.strip())

            if not os.path.exists(csv_path):
                return "{}", f"File not found: {csv_path}", 0

            should_reload = (
                self.df is None or
                not hasattr(self, '_last_csv_path') or
                self._last_csv_path != csv_path or
                getattr(self, '_last_delimiter', None) != delimiter or
                getattr(self, '_last_encoding', None) != encoding
            )

            if should_reload:
                self.df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
                self._last_csv_path = csv_path
                self._last_delimiter = delimiter
                self._last_encoding = encoding

            row_count = len(self.df)

            if selected_row < 0:
                selected_row = 0
            if selected_row >= row_count:
                selected_row = 0

            row_dict = self.df.iloc[selected_row].to_dict()
            json_output = json.dumps(row_dict, indent=2, ensure_ascii=False)

            return json_output, "", row_count

        except Exception as e:
            return "{}", str(e), 0


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "APZmediaDynamicCSVReader": APZmediaDynamicCSVReader,
    "APZmediaCSVReader": APZmediaCSVReader,
    "APZmediaCSVColumnExtractor": APZmediaCSVColumnExtractor,
    "APZmediaCSVReaderAdvanced": APZmediaCSVReaderAdvanced,
    "APZmediaCSVToJSON": APZmediaCSVToJSON,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APZmediaDynamicCSVReader": "APZmedia Dynamic CSV Reader",
    "APZmediaCSVReader": "APZmedia CSV Reader",
    "APZmediaCSVColumnExtractor": "APZmedia CSV Column Extractor",
    "APZmediaCSVReaderAdvanced": "APZmedia CSV Reader Advanced",
    "APZmediaCSVToJSON": "APZmedia CSV to JSON",
}
