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
    """Truly dynamic CSV Reader that regenerates outputs based on CSV structure"""
    
    def __init__(self):
        self.df = None
        self.column_names = []
        self.row_count = 0
        self.current_row = 0
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": "", "tooltip": "Path to the CSV file"}),
                "selected_row": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1, "tooltip": "Row index to extract (0-based)"}),
                "delimiter": ("STRING", {"default": ",", "tooltip": "CSV delimiter character"}),
                "encoding": ("STRING", {"default": "utf-8", "tooltip": "File encoding"}),
                "refresh_csv": ("BOOLEAN", {"default": False, "tooltip": "Click to refresh CSV data and regenerate outputs"}),
            }
        }
    
    # Dynamic return types based on stored DataFrame
    @classmethod
    def RETURN_TYPES(cls):
        # Start with base outputs, will be expanded dynamically
        return ("STRING", "INT", "STRING", "STRING", "STRING")
    
    @classmethod
    def RETURN_NAMES(cls):
        # Start with base output names, will be expanded dynamically
        return ("column_names", "row_count", "csv_info", "error_message", "csv_data_json")
    
    FUNCTION = "read_csv_dynamic"
    CATEGORY = "APZmedia/CSV Utils"
    
    def read_csv_dynamic(self, csv_path: str, selected_row: int, delimiter: str = ",", 
                        encoding: str = "utf-8", refresh_csv: bool = False) -> tuple:
        """
        Dynamic CSV reading with stored DataFrame and regenerated outputs
        
        Args:
            csv_path: Path to the CSV file
            selected_row: Row index to extract (0-based)
            delimiter: CSV delimiter character
            encoding: File encoding
            refresh_csv: Boolean to trigger CSV refresh and output regeneration
            
        Returns:
            tuple: Dynamic outputs based on CSV structure
        """
        try:
            # Check if file exists
            if not csv_path or not os.path.exists(csv_path):
                return "No file", 0, "File not found", "File not found", "{}"
            
            # Load or refresh DataFrame
            if refresh_csv or self.df is None:
                self.df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
                self.column_names = self.df.columns.tolist()
                self.row_count = len(self.df)
                print(f"CSV loaded: {len(self.column_names)} columns, {self.row_count} rows")
            
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
            
            # Create dynamic outputs based on actual columns
            outputs = [column_names_str, self.row_count, csv_info, "", row_data_json]
            
            # Add individual column outputs
            for col_name in self.column_names:
                value = self.df.iloc[selected_row][col_name]
                if pd.isna(value):
                    outputs.append("")
                else:
                    outputs.append(str(value))
            
            return tuple(outputs)
            
        except Exception as e:
            return "Error", 0, "Error occurred", str(e), "{}"
    
    # Method to get dynamic return types based on stored DataFrame
    def get_return_types(self):
        """Get dynamic return types based on stored DataFrame"""
        if self.df is None:
            return ("STRING", "INT", "STRING", "STRING", "STRING")
        
        # Base types + one STRING for each column
        base_types = ("STRING", "INT", "STRING", "STRING", "STRING")
        column_types = ("STRING",) * len(self.column_names)
        return base_types + column_types
    
    def get_return_names(self):
        """Get dynamic return names based on stored DataFrame"""
        if self.df is None:
            return ("column_names", "row_count", "csv_info", "error_message", "csv_data_json")
        
        # Base names + actual column names
        base_names = ("column_names", "row_count", "csv_info", "error_message", "csv_data_json")
        return base_names + tuple(self.column_names)


class APZmediaCSVReader:
    """Clean CSV Reader that outputs JSON data for easy access"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_path": ("STRING", {"default": "", "tooltip": "Path to the CSV file"}),
                "selected_row": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1, "tooltip": "Row index to extract (0-based)"}),
                "delimiter": ("STRING", {"default": ",", "tooltip": "CSV delimiter character"}),
                "encoding": ("STRING", {"default": "utf-8", "tooltip": "File encoding"}),
                "refresh_csv": ("BOOLEAN", {"default": False, "tooltip": "Click to refresh CSV data"}),
            }
        }
    
    # Clean, minimal outputs - no clutter
    RETURN_TYPES = ("STRING", "INT", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("column_names", "row_count", "csv_info", "error_message", "row_data_json")
    FUNCTION = "read_csv"
    CATEGORY = "APZmedia/CSV Utils"
    
    def read_csv(self, csv_path: str, selected_row: int, delimiter: str = ",", 
                encoding: str = "utf-8", refresh_csv: bool = False) -> tuple:
        """
        Read CSV file and return structured data
        
        Args:
            csv_path: Path to the CSV file
            selected_row: Row index to extract (0-based)
            delimiter: CSV delimiter character
            encoding: File encoding
            refresh_csv: Boolean to trigger CSV refresh
            
        Returns:
            tuple: (column_names, row_count, csv_info, error_message, row_data_json)
        """
        try:
            # Check if file exists
            if not csv_path or not os.path.exists(csv_path):
                return "No file", 0, "File not found", "File not found", "{}"
            
            # Read CSV file
            df = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
            
            # Get column names and row count
            column_names = ", ".join(df.columns.tolist())
            row_count = len(df)
            
            # Validate selected row
            if selected_row >= row_count:
                selected_row = 0
            
            # Create CSV info
            csv_info = f"File: {os.path.basename(csv_path)} | Rows: {row_count} | Columns: {len(df.columns)} | Selected Row: {selected_row}"
            
            # Convert selected row to JSON for easy access
            row_dict = df.iloc[selected_row].to_dict()
            row_data_json = json.dumps(row_dict, indent=2, ensure_ascii=False)
            
            return column_names, row_count, csv_info, "", row_data_json
            
        except Exception as e:
            return "Error", 0, "Error occurred", str(e), "{}"


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