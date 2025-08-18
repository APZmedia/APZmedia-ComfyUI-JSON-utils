"""
APZmedia CSV Reader Node
Reads CSV files and provides dynamic outputs for each column
"""

import csv
import os
import pandas as pd
import json
from typing import Any, Dict, List, Optional, Tuple, Union


class APZmediaDynamicCSVReader:
    """Truly Dynamic CSV Reader that adapts output structure based on CSV columns"""
    
    def __init__(self):
        self.df = None
        self.column_names = []
        self.row_count = 0
        self.current_row = 0
        self._cached_return_types = None
        self._cached_return_names = None
    
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
    
    @classmethod
    def RETURN_TYPES(cls):
        # Base return types - will be extended dynamically
        return ("STRING", "INT", "STRING", "STRING", "STRING")
    
    @classmethod
    def RETURN_NAMES(cls):
        # Base return names - will be extended dynamically
        return ("column_names", "row_count", "csv_info", "error_message", "csv_data_json")
    
    FUNCTION = "read_csv_dynamic"
    CATEGORY = "APZmedia/CSV Utils"
    
    def read_csv_dynamic(self, csv_path: str, selected_row: int, delimiter: str = ",", 
                        encoding: str = "utf-8", refresh_trigger: str = "") -> tuple:
        """
        Dynamic CSV reading with adaptive output structure
        
        Args:
            csv_path: Path to the CSV file
            selected_row: Row index to extract (0-based)
            delimiter: CSV delimiter character
            encoding: File encoding
            refresh_trigger: Trigger for forcing reload
            
        Returns:
            tuple: Dynamic outputs based on CSV structure
        """
        try:
            # Check if file exists
            if not csv_path or not os.path.exists(csv_path):
                return ("No file", 0, "File not found", "File not found", "{}")
            
            # Load or refresh DataFrame when file path changes, DataFrame is None, or refresh_trigger changes
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
                
                # Update cached return types and names
                self._update_return_structure()
                
                print(f"CSV loaded: {len(self.column_names)} columns, {self.row_count} rows")
                print(f"Columns: {', '.join(self.column_names)}")
                if refresh_trigger:
                    print("CSV reloaded via button click - structure updated!")
            
            # Validate selected row
            if selected_row >= self.row_count:
                selected_row = 0
            self.current_row = selected_row
            
            # Get basic info
            column_names_str = ", ".join(self.column_names)
            csv_info = f"File: {os.path.basename(csv_path)} | Rows: {self.row_count} | Columns: {len(self.column_names)} | Selected Row: {selected_row}"
            
            # Convert selected row to JSON
            row_dict = self.df.iloc[selected_row].to_dict()
            row_data_json = json.dumps(row_dict, indent=2, ensure_ascii=False)
            
            # Create base outputs
            outputs = [column_names_str, self.row_count, csv_info, "", row_data_json]
            
            # Add individual column values
            for col_name in self.column_names:
                value = self.df.iloc[selected_row][col_name]
                if pd.isna(value):
                    outputs.append("")
                else:
                    outputs.append(str(value))
            
            return tuple(outputs)
            
        except Exception as e:
            print(f"Error in CSV reader: {e}")
            return ("Error", 0, "Error occurred", str(e), "{}")
    
    def _update_return_structure(self):
        """Update the cached return types and names based on current CSV structure"""
        if self.df is not None:
            # Base types and names
            base_types = ("STRING", "INT", "STRING", "STRING", "STRING")
            base_names = ("column_names", "row_count", "csv_info", "error_message", "csv_data_json")
            
            # Add one STRING output for each column
            column_types = ("STRING",) * len(self.column_names)
            column_names = tuple(self.column_names)
            
            self._cached_return_types = base_types + column_types
            self._cached_return_names = base_names + column_names
            
            print(f"Updated return structure: {len(self._cached_return_types)} outputs")
            print(f"Column outputs: {', '.join(column_names)}")


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
        """
        CSV reading with fixed output structure (25 column outputs max)
        
        Args:
            csv_path: Path to the CSV file
            selected_row: Row index to extract (0-based)
            delimiter: CSV delimiter character
            encoding: File encoding
            refresh_trigger: Internal trigger for button updates
            
        Returns:
            tuple: Fixed outputs with up to 25 column values
        """
        try:
            # Check if file exists
            if not csv_path or not os.path.exists(csv_path):
                error_outputs = ["No file", 0, "File not found", "File not found", "{}"] + [""] * 25
                return tuple(error_outputs)
            
            # Load or refresh DataFrame when file path changes, DataFrame is None, or refresh_trigger changes
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
            
            # Validate selected row
            if selected_row >= self.row_count:
                selected_row = 0
            self.current_row = selected_row
            
            # Get basic info
            column_names_str = ", ".join(self.column_names)
            csv_info = f"File: {os.path.basename(csv_path)} | Rows: {self.row_count} | Columns: {len(self.column_names)} | Selected Row: {selected_row}"
            
            # Convert selected row to JSON
            row_dict = self.df.iloc[selected_row].to_dict()
            row_data_json = json.dumps(row_dict, indent=2, ensure_ascii=False)
            
            # Create outputs with individual column values
            outputs = [column_names_str, self.row_count, csv_info, "", row_data_json]
            
            # Add individual column values (up to 25 columns)
            for i in range(25):
                if i < len(self.column_names):
                    value = self.df.iloc[selected_row][self.column_names[i]]
                    if pd.isna(value):
                        outputs.append("")
                    else:
                        outputs.append(str(value))
                else:
                    outputs.append("")  # Empty for unused columns
            
            return tuple(outputs)
            
        except Exception as e:
            # Return correct number of outputs even on error
            error_outputs = ["Error", 0, "Error occurred", str(e), "{}"] + [""] * 25
            return tuple(error_outputs)
    




class APZmediaCSVColumnExtractor:
    """Extract specific columns by name from CSV"""
    
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
    
    # Fixed number of outputs for specific columns
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("column_names", "row_count", "csv_info", "error_message", "col_1", "col_2", "col_3")
    FUNCTION = "extract_columns"
    CATEGORY = "APZmedia/CSV Utils"
    
    def extract_columns(self, csv_path: str, selected_row: int, column_names: str,
                       delimiter: str = ",", encoding: str = "utf-8") -> tuple:
        """
        Extract specific columns by name from CSV
        
        Args:
            csv_path: Path to the CSV file
            selected_row: Row index to extract (0-based)
            column_names: Comma-separated column names
            delimiter: CSV delimiter character
            encoding: File encoding
            
        Returns:
            tuple: (column_names, row_count, csv_info, error_message, col_1, col_2, col_3)
        """
        try:
            # Check if file exists
            if not csv_path or not os.path.exists(csv_path):
                return "No file", 0, "File not found", "File not found", "", "", ""
            
            # Read CSV file
            df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
            
            # Get basic info
            all_column_names = ", ".join(df.columns.tolist())
            row_count = len(df)
            
            # Parse requested column names
            requested_cols = [col.strip() for col in column_names.split(",")]
            
            # Validate selected row
            if selected_row >= row_count:
                selected_row = 0
            
            # Create CSV info
            csv_info = f"File: {os.path.basename(csv_path)} | Rows: {row_count} | Columns: {len(df.columns)} | Selected Row: {selected_row}"
            
            # Extract values for requested columns (up to 3)
            extracted_values = []
            for i, col_name in enumerate(requested_cols[:3]):  # Limit to 3 columns
                if col_name in df.columns:
                    value = df.iloc[selected_row][col_name]
                    if pd.isna(value):
                        extracted_values.append("")
                    else:
                        extracted_values.append(str(value))
                else:
                    extracted_values.append(f"(Column '{col_name}' not found)")
            
            # Pad with empty strings if less than 3 columns
            while len(extracted_values) < 3:
                extracted_values.append("")
            
            return all_column_names, row_count, csv_info, "", *extracted_values
            
        except Exception as e:
            return "Error", 0, "Error occurred", str(e), "", "", ""


class APZmediaCSVReaderAdvanced:
    """Advanced CSV reader with more flexible column handling"""
    
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
        """
        Advanced CSV reading with column selection
        
        Args:
            csv_path: Path to the CSV file
            selected_row: Row index to extract (0-based)
            column_indices: Comma-separated column indices
            delimiter: CSV delimiter character
            encoding: File encoding
            
        Returns:
            tuple: (column_names, row_count, selected_columns, row_data, csv_info, error_message, status)
        """
        try:
            # Check if file exists
            if not csv_path or not os.path.exists(csv_path):
                return "No file", 0, "", "", "", "File not found", "error"
            
            # Read CSV file
            df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
            
            # Get basic info
            column_names = ", ".join(df.columns.tolist())
            row_count = len(df)
            
            # Parse column indices
            try:
                indices = [int(idx.strip()) for idx in column_indices.split(",") if idx.strip()]
            except ValueError:
                indices = [0, 1, 2]  # Default to first 3 columns
            
            # Validate selected row
            if selected_row >= row_count:
                selected_row = 0
            
            # Extract selected columns
            selected_cols = []
            row_data_parts = []
            
            for idx in indices:
                if 0 <= idx < len(df.columns):
                    col_name = df.columns[idx]
                    selected_cols.append(col_name)
                    
                    value = df.iloc[selected_row, idx]
                    if pd.isna(value):
                        row_data_parts.append("(empty)")
                    else:
                        row_data_parts.append(str(value))
                else:
                    selected_cols.append(f"col_{idx}")
                    row_data_parts.append("(invalid)")
            
            selected_columns = ", ".join(selected_cols)
            row_data = " | ".join(row_data_parts)
            
            # Create CSV info
            csv_info = f"File: {os.path.basename(csv_path)} | Rows: {row_count} | Columns: {len(df.columns)} | Selected Row: {selected_row}"
            
            return column_names, row_count, selected_columns, row_data, csv_info, "", "success"
            
        except Exception as e:
            return "Error", 0, "", "", "", str(e), "error"


class APZmediaCSVToJSON:
    """Convert CSV data to JSON format"""
    
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
        """
        Convert CSV row to JSON format
        
        Args:
            csv_path: Path to the CSV file
            selected_row: Row index to convert (0-based)
            delimiter: CSV delimiter character
            encoding: File encoding
            
        Returns:
            tuple: (json_output, error_message, row_count)
        """
        try:
            # Check if file exists
            if not csv_path or not os.path.exists(csv_path):
                return "{}", "File not found", 0
            
            # Read CSV file
            df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
            row_count = len(df)
            
            # Validate selected row
            if selected_row >= row_count:
                selected_row = 0
            
            # Convert selected row to dictionary
            row_dict = df.iloc[selected_row].to_dict()
            
            # Convert to JSON
            import json
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
