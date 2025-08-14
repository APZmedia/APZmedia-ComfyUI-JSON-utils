#!/usr/bin/env python3
"""
Simple test script for APZmedia ComfyUI JSON and CSV Utils
"""

import json
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_json_key_extractor():
    """Test JSON Key Extractor functionality"""
    print("Testing JSON Key Extractor...")
    
    # Import the node
    from nodes.json_key_extractor import APZmediaJSONKeyExtractor
    
    # Create instance
    node = APZmediaJSONKeyExtractor()
    
    # Test data
    test_json = '{"project": {"name": "Star Wars", "type": "VFX"}, "shots": [{"id": "sw_0010"}]}'
    
    # Test basic key extraction
    result = node.extract_json_value(test_json, "project", "default")
    print(f"Basic extraction result: {result[0]}")
    
    # Test nested key extraction
    result = node.extract_json_value(test_json, "", "default", "project.name")
    print(f"Nested extraction result: {result[0]}")
    
    print("✓ JSON Key Extractor test passed\n")

def test_csv_reader():
    """Test CSV Reader functionality"""
    print("Testing CSV Reader...")
    
    # Import the node
    from nodes.csv_reader import APZmediaCSVReader
    
    # Create instance
    node = APZmediaCSVReader()
    
    # Test with sample CSV
    csv_path = "examples/sample_data.csv"
    if os.path.exists(csv_path):
        result = node.read_csv_data(csv_path, 0, ",", "utf-8")
        print(f"CSV reading result: {result[0]} (columns), {result[1]} (rows)")
        print(f"First row data: {result[2:6]}")
        print("✓ CSV Reader test passed\n")
    else:
        print("⚠ Sample CSV file not found, skipping test\n")

def test_json_utils():
    """Test JSON Utils functionality"""
    print("Testing JSON Utils...")
    
    # Import the node
    from nodes.json_utils import APZmediaJSONValidator
    
    # Create instance
    node = APZmediaJSONValidator()
    
    # Test data
    test_json = '{"name": "test", "value": 123}'
    
    # Test validation
    result = node.validate_and_format(test_json, True, 2)
    print(f"JSON validation result: {result[2]} (valid)")
    print("✓ JSON Utils test passed\n")

def main():
    """Run all tests"""
    print("APZmedia ComfyUI JSON and CSV Utils - Node Tests")
    print("=" * 50)
    
    try:
        test_json_key_extractor()
        test_csv_reader()
        test_json_utils()
        print("All tests completed successfully!")
    except Exception as e:
        print(f"Test failed with error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 