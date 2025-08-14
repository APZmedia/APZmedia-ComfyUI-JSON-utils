# APZmedia ComfyUI JSON and CSV Utility Nodes

## Overview

This package provides a comprehensive set of utility nodes for ComfyUI that streamline JSON and CSV data processing for VFX workflows. The tools include **JSON Key Extractor**, **CSV Reader**, and other data processing utilities designed to integrate seamlessly with ComfyUI's node-based workflow system.

## Features

### 1. **APZmedia JSON Key Extractor**

* **Dynamic Key Input**: Define JSON keys through widgets for flexible data extraction
* **JSON Validation**: Validates input JSON and provides error handling
* **Multiple Output Types**: Supports string, number, boolean, and object outputs
* **Nested Key Support**: Extract values from nested JSON structures
* **Default Values**: Provide fallback values when keys don't exist

### 2. **APZmedia Dynamic CSV Reader**

* **File Path Input**: Accept CSV file paths as input
* **Dynamic Column Outputs**: Creates individual outputs for each column (up to 50 columns)
* **Row Selection**: Select specific rows to extract data
* **Configurable Column Limit**: Set maximum number of columns to process
* **Error Handling**: Graceful handling of file errors and malformed CSV data
* **Multiple Data Types**: Support for different column data types
* **Direct Output Access**: Each column value available as a separate output

## Input and Output Types

### **APZmedia JSON Key Extractor**

* **Input Types**:  
   * `json_input` (STRING): The JSON string to parse
   * `key_name` (STRING): The key to extract from the JSON (widget)
   * `default_value` (STRING): Default value if key doesn't exist
* **Output Types**:  
   * `extracted_value` (STRING): The extracted value as a string
   * `value_type` (STRING): The type of the extracted value

### **APZmedia Dynamic CSV Reader**

* **Input Types**:  
   * `csv_path` (STRING): Path to the CSV file
   * `selected_row` (INT): Row index to extract (0-based)
   * `delimiter` (STRING): CSV delimiter character
   * `encoding` (STRING): File encoding
   * `max_columns` (INT): Maximum number of columns to support (1-50)
* **Output Types**:  
   * `column_names` (STRING): List of column names
   * `row_count` (INT): Total number of rows in CSV
   * `csv_info` (STRING): File information and statistics
   * `error_message` (STRING): Any error messages
   * `col_1` through `col_50`: Values from each column (unused columns are empty)

## How They Work

### **APZmedia JSON Key Extractor**

1. **JSON Parsing**: Validates and parses the input JSON string
2. **Key Extraction**: Searches for the specified key in the JSON structure
3. **Type Detection**: Determines the data type of the extracted value
4. **Default Handling**: Returns default value if key is not found
5. **Output Generation**: Provides the extracted value and its type

### **APZmedia Dynamic CSV Reader**

1. **File Reading**: Reads the CSV file from the specified path
2. **Column Detection**: Analyzes the CSV structure to identify columns
3. **Dynamic Output Creation**: Creates up to 50 individual outputs for columns
4. **Row Selection**: Extracts data from the selected row
5. **Data Distribution**: Outputs each column's value to its respective output (col_1, col_2, etc.)

## Use Cases

### **JSON Data Processing**

* Extract configuration values from JSON files
* Parse API responses in ComfyUI workflows
* Handle nested data structures
* Provide fallback values for missing data

### **CSV Data Integration**

* Import shot lists and project data
* Process animation curves and keyframe data
* Handle batch processing parameters
* Integrate external data sources

### **Workflow Integration**

* Chain JSON extractors for complex data processing
* Use CSV data to drive parameter variations
* Combine with image generation for data-driven workflows
* Create dynamic naming schemes based on external data

## Installation

1. **Clone or download** this repository to your ComfyUI `custom_nodes` directory
2. **Install dependencies**: `pip install -e .`
3. **Restart ComfyUI** to load the new utility nodes
4. **Find tools** in the "APZmedia" category in the node menu

## Dependencies

* `json`: For JSON parsing and validation
* `csv`: For CSV file reading and processing
* `pandas`: For advanced CSV processing (optional)
* `ComfyUI`: The main application

## License

MIT License - See LICENSE file for details.

## Author

**Pablo Apiolazza** - APZmedia

## Support

For issues, feature requests, or questions, please visit the GitHub repository.

## About

A collection of ComfyUI nodes for JSON and CSV data processing in VFX workflows. 