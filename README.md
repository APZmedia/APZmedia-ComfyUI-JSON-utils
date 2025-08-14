# APZmedia ComfyUI JSON and CSV Utility Nodes

A collection of utility nodes for JSON and CSV data processing in ComfyUI workflows. Features dynamic CSV reading with real-time button updates and comprehensive JSON processing capabilities.

## Overview

This package provides a comprehensive set of utility nodes for ComfyUI that streamline JSON and CSV data processing for VFX workflows. The tools include **JSON Key Extractor**, **Dynamic CSV Reader**, and other data processing utilities designed to integrate seamlessly with ComfyUI's node-based workflow system.

## Features

### 1. **APZmedia JSON Key Extractor**

* **Dynamic Key Input**: Define JSON keys through widgets for flexible data extraction
* **JSON Validation**: Validates input JSON and provides error handling
* **Multiple Output Types**: Supports string, number, boolean, and object outputs
* **Nested Key Support**: Extract values from nested JSON structures
* **Default Values**: Provide fallback values when keys don't exist

### 2. **APZmedia CSV Reader**

* **File Path Input**: Accept CSV file paths as input
* **Real Update Button**: Click "🔄 Update CSV" button to reload data
* **Session Storage**: Maintains data in memory for performance
* **Row Selection**: Select specific rows to extract data
* **JSON Output**: Returns CSV data as structured JSON for easy access
* **Error Handling**: Graceful handling of file errors and malformed CSV data
* **Multiple Formats**: Supports various CSV delimiters and encodings

## Input and Output Types

### **APZmedia JSON Key Extractor**

* **Input Types**:  
   * `json_input` (STRING): The JSON string to parse
   * `key_name` (STRING): The key to extract from the JSON (widget)
   * `default_value` (STRING): Default value if key doesn't exist
* **Output Types**:  
   * `extracted_value` (STRING): The extracted value as a string
   * `value_type` (STRING): The type of the extracted value

### **APZmedia CSV Reader**

* **Input Types**:  
   * `csv_path` (STRING): Path to the CSV file
   * `selected_row` (INT): Row index to extract (0-based)
   * `delimiter` (STRING): CSV delimiter character
   * `encoding` (STRING): File encoding
   * `force_reload` (INT): Internal parameter for button trigger
* **Output Types**:  
   * `column_names` (STRING): List of column names
   * `row_count` (INT): Total number of rows in CSV
   * `csv_info` (STRING): File information and statistics
   * `error_message` (STRING): Any error messages
   * `csv_data_json` (STRING): Selected row data as JSON string

## How They Work

### **APZmedia JSON Key Extractor**

1. **JSON Parsing**: Validates and parses the input JSON string
2. **Key Extraction**: Searches for the specified key in the JSON structure
3. **Type Detection**: Determines the data type of the extracted value
4. **Default Handling**: Returns default value if key is not found
5. **Output Generation**: Provides the extracted value and its type

### **APZmedia CSV Reader**

1. **File Reading**: Reads the CSV file from the specified path
2. **Session Storage**: Maintains DataFrame in memory for performance
3. **Button Trigger**: "🔄 Update CSV" button increments force_reload parameter
4. **Row Selection**: Extracts data from the selected row
5. **JSON Output**: Converts row data to JSON string for easy access

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

### Method 1: ComfyUI Manager (Recommended)
1. Open ComfyUI
2. Go to Manager → Install
3. Search for "APZmedia JSON Utils"
4. Click Install

### Method 2: Manual Installation
1. Clone this repository to your ComfyUI `custom_nodes` directory:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/APZmedia/ComfyUI-APZmedia-JSON-utils.git
   ```
2. Install dependencies:
   ```bash
   cd ComfyUI-APZmedia-JSON-utils
   pip install -r requirements.txt
   ```
3. Restart ComfyUI to load the new utility nodes
4. Find tools in the "APZmedia" category in the node menu

## Dependencies

* `pandas>=1.3.0`: For advanced CSV processing and data manipulation
* `ComfyUI`: The main application

## Features

### 🎯 **Dynamic CSV Reader with Real Buttons**
- **Real Update Button**: Click "🔄 Update CSV" button to reload data
- **Dynamic Outputs**: Automatically creates outputs based on CSV columns
- **Session Storage**: Maintains data in memory for performance
- **Multiple Formats**: Supports various CSV delimiters and encodings

### 🔧 **JSON Processing Utilities**
- **Key Extraction**: Extract values from JSON using dynamic key names
- **Multi-Key Support**: Extract multiple keys simultaneously
- **Nested Path Support**: Access deeply nested JSON values
- **Validation**: Built-in JSON validation and error handling

### 📊 **Sample Data Included**
- Multiple CSV examples for testing different scenarios
- JSON sample files for validation
- Comprehensive test scripts

## License

MIT License - See LICENSE file for details.

## Author

**Pablo Apiolazza** - APZmedia

## Support

For issues, feature requests, or questions, please visit the GitHub repository.

## About

A collection of ComfyUI nodes for JSON and CSV data processing in VFX workflows. 