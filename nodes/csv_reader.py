"""
APZmedia CSV Reader Node
Reads CSV files and provides dynamic outputs for each column
"""

import csv
import os
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple, Union


class APZmediaCSVReader:
    """Read CSV files and provide dynamic outputs for each column"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": "", "tooltip": "Path to the CSV file"}),
                "selected_row": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "delimiter": ("STRING", {"default": ",", "tooltip": "CSV delimiter character"}),
                "encoding": ("STRING", {"default": "utf-8", "tooltip": "File encoding"}),
            },
            "optional": {
                "update_csv": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("column_names", "row_count", "col_1", "col_2", "col_3", "col_4", "col_5", "col_6", "col_7", "col_8")
    FUNCTION = "read_csv_data"
    CATEGORY = "APZmedia/CSV Utils"
    
    def read_csv_data(self, csv_path: str, selected_row: int, delimiter: str = ",", 
                     encoding: str = "utf-8", update_csv: bool = False) -> tuple:
        """
        Read CSV file and extract data from selected row
        
        Args:
            csv_path: Path to the CSV file
            selected_row: Row index to extract (0-based)
            delimiter: CSV delimiter character
            encoding: File encoding
            update_csv: Boolean to trigger CSV refresh
            
        Returns:
            tuple: (column_names, row_count, col_1, col_2, ..., col_8)
        """
        try:
            # Check if file exists
            if not csv_path or not os.path.exists(csv_path):
                return "No file", 0, "", "", "", "", "", "", "", ""
            
            # Read CSV file
            df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
            
            # Get column names and row count
            column_names = ", ".join(df.columns.tolist())
            row_count = len(df)
            
            # Validate selected row
            if selected_row >= row_count:
                selected_row = 0
            
            # Extract values from selected row
            row_values = []
            for i in range(8):  # Support up to 8 columns
                if i < len(df.columns):
                    value = df.iloc[selected_row, i]
                    # Handle NaN values
                    if pd.isna(value):
                        row_values.append("")
                    else:
                        row_values.append(str(value))
                else:
                    row_values.append("")
            
            return (column_names, row_count) + tuple(row_values)
            
        except Exception as e:
            return f"Error: {str(e)}", 0, "", "", "", "", "", "", "", ""


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
                        row_data_parts.append(f"{col_name}: (empty)")
                    else:
                        row_data_parts.append(f"{col_name}: {str(value)}")
                else:
                    selected_cols.append(f"col_{idx}")
                    row_data_parts.append(f"col_{idx}: (invalid)")
            
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
    "APZmediaCSVReader": APZmediaCSVReader,
    "APZmediaCSVReaderAdvanced": APZmediaCSVReaderAdvanced,
    "APZmediaCSVToJSON": APZmediaCSVToJSON,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APZmediaCSVReader": "APZmedia CSV Reader",
    "APZmediaCSVReaderAdvanced": "APZmedia CSV Reader Advanced",
    "APZmediaCSVToJSON": "APZmedia CSV to JSON",
} 