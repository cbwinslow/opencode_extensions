#!/usr/bin/env python3

import json
import sys

def load_openapi(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def validate_openapi(spec):
    issues = []
    if 'openapi' not in spec:
        issues.append("Missing 'openapi' field.")
    if 'info' not in spec:
        issues.append("Missing 'info' section.")
    if 'paths' not in spec:
        issues.append("Missing 'paths' section.")
    # Add more validations as needed
    return issues

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python openapi_validator.py <openapi_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    try:
        spec = load_openapi(file_path)
        issues = validate_openapi(spec)
        if issues:
            print("Validation issues:")
            for issue in issues:
                print(f"- {issue}")
        else:
            print("OpenAPI spec is valid.")
    except Exception as e:
        print(f"Error: {e}")