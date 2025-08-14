# APZmedia ComfyUI JSON and CSV Utils - Usage Guide

## Overview

This guide provides detailed instructions on how to use the APZmedia JSON and CSV utility nodes in ComfyUI workflows.

## JSON Utility Nodes

### 1. APZmedia JSON Key Extractor

**Purpose**: Extract specific values from JSON data using dynamic key widgets.

**Inputs**:
- `json_input`: JSON string to parse
- `key_name`: Key to extract (widget input)
- `default_value`: Default value if key doesn't exist
- `nested_key_path`: Dot notation for nested keys (e.g., 'user.profile.name')

**Outputs**:
- `extracted_value`: The extracted value as a string
- `value_type`: Type of the extracted value
- `error_message`: Any error messages

**Example Usage**:
```
JSON Input: {"project": {"name": "Star Wars", "type": "VFX"}}
Key Name: project
Result: {"name": "Star Wars", "type": "VFX"}

Nested Key Path: project.name
Result: Star Wars
```

### 2. APZmedia JSON Multi-Key Extractor

**Purpose**: Extract multiple values from JSON using multiple key widgets.

**Inputs**:
- `json_input`: JSON string to parse
- `key_1` through `key_5`: Individual keys to extract
- `default_value`: Default value for missing keys

**Outputs**:
- `value_1` through `value_5`: Extracted values for each key

**Example Usage**:
```
JSON Input: {"name": "John", "age": 30, "city": "NYC"}
Key 1: name
Key 2: age
Key 3: city
Result: value_1="John", value_2="30", value_3="NYC"
```

### 3. APZmedia JSON Validator

**Purpose**: Validate and format JSON strings.

**Inputs**:
- `json_input`: JSON string to validate
- `format_output`: Whether to format the output
- `indent_size`: Number of spaces for indentation

**Outputs**:
- `formatted_json`: Formatted JSON string
- `error_message`: Validation errors
- `is_valid`: Boolean indicating if JSON is valid

### 4. APZmedia JSON Merger

**Purpose**: Merge multiple JSON objects.

**Inputs**:
- `json_1` through `json_4`: JSON strings to merge
- `merge_strategy`: How to handle conflicts (replace, combine, deep_merge)

**Outputs**:
- `merged_json`: Combined JSON result
- `error_message`: Any error messages

### 5. APZmedia JSON Path Extractor

**Purpose**: Extract values using JSONPath expressions.

**Inputs**:
- `json_input`: JSON string to parse
- `json_path`: JSONPath expression (e.g., "$.user.name", "$[*].id")
- `default_value`: Default value if path not found

**Outputs**:
- `extracted_value`: The extracted value
- `value_type`: Type of the extracted value
- `error_message`: Any error messages

## CSV Utility Nodes

### 1. APZmedia Dynamic CSV Reader

**Purpose**: Read CSV files and provide individual outputs for each column.

**Inputs**:
- `csv_path`: Path to the CSV file
- `selected_row`: Row index to extract (0-based)
- `delimiter`: CSV delimiter character
- `encoding`: File encoding
- `max_columns`: Maximum number of columns to support (1-50)

**Outputs**:
- `column_names`: List of column names
- `row_count`: Total number of rows
- `csv_info`: File information and statistics
- `error_message`: Any error messages
- `col_1` through `col_50`: Values from each column (unused columns are empty)

**Example Usage**:
```
CSV File: examples/sample_data.csv
Selected Row: 1
Result: 
  column_names: "Group,Prompt,Neg-Prompt,Aspect-ratio,Height,Width,seed,seed-mode,cfg,seed-type"
  row_count: 5
  csv_info: "File: sample_data.csv | Rows: 5 | Columns: 10 | Selected Row: 1"
  col_1: "Character"
  col_2: "Portrait of a warrior, detailed armor, dramatic lighting"
  col_3: "blurry, low quality, distorted"
  col_4: "4:3"
  col_5: "1024"
  col_6: "768"
  col_7: "67890"
  col_8: "fixed"
  col_9: "8.0"
  col_10: "normal"
  col_11 through col_50: "" (empty for unused columns)
```

### 2. APZmedia CSV Reader Advanced

**Purpose**: Advanced CSV reading with flexible column selection.

**Inputs**:
- `csv_path`: Path to the CSV file
- `selected_row`: Row index to extract
- `column_indices`: Comma-separated column indices (e.g., "0,1,2")
- `delimiter`: CSV delimiter character
- `encoding`: File encoding

**Outputs**:
- `column_names`: List of all column names
- `row_count`: Total number of rows
- `selected_columns`: Names of selected columns
- `row_data`: Formatted row data
- `csv_info`: File information
- `error_message`: Any error messages
- `status`: Success/error status

### 3. APZmedia CSV to JSON

**Purpose**: Convert CSV row data to JSON format.

**Inputs**:
- `csv_path`: Path to the CSV file
- `selected_row`: Row index to convert
- `delimiter`: CSV delimiter character
- `encoding`: File encoding

**Outputs**:
- `json_output`: JSON representation of the row
- `error_message`: Any error messages
- `row_count`: Total number of rows

## Workflow Examples

### Example 1: JSON Configuration Processing

```
1. Load JSON configuration file
2. Use JSON Key Extractor to get project name
3. Use JSON Path Extractor to get shot list
4. Process each shot with other nodes
```

### Example 2: CSV Shot List Processing

```
1. Load CSV shot list
2. Use CSV Reader to extract shot data
3. Use JSON Key Extractor to process shot parameters
4. Generate filenames based on shot data
```

### Example 3: Data Validation Workflow

```
1. Load JSON data
2. Use JSON Validator to check format
3. Use JSON Key Extractor to validate required fields
4. Process only valid data
```

## Best Practices

### JSON Processing
1. Always validate JSON input before processing
2. Use nested key paths for complex data structures
3. Provide meaningful default values
4. Handle error cases gracefully

### CSV Processing
1. Check file existence before reading
2. Validate row indices to avoid out-of-bounds errors
3. Handle different CSV formats (delimiters, encodings)
4. Use appropriate column selection for your data

### General Tips
1. Chain nodes logically for complex data processing
2. Use error outputs to handle failures gracefully
3. Test with sample data before using in production
4. Consider data types when processing extracted values

## Troubleshooting

### Common Issues

**JSON Parsing Errors**:
- Check JSON syntax validity
- Ensure proper escaping of special characters
- Verify JSON structure matches expected format

**CSV Reading Errors**:
- Verify file path is correct
- Check file encoding (UTF-8 recommended)
- Ensure delimiter matches CSV format
- Validate row index is within bounds

**Key Extraction Issues**:
- Verify key exists in JSON structure
- Check for typos in key names
- Use nested key paths for complex structures
- Provide fallback default values

### Error Messages

- `"Invalid JSON"`: JSON syntax error
- `"File not found"`: CSV file path issue
- `"Key not found"`: Missing JSON key
- `"Index out of bounds"`: Invalid row/column index

## Sample Data

The `examples/` directory contains sample files for testing:
- `sample_data.json`: Sample JSON with project and shot data
- `sample_data.csv`: Sample CSV with shot information

Use these files to test and understand the node functionality before integrating into your workflows. 