#!/usr/bin/env python3

import json
import sys

def convert_json(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Converted {input_file} to formatted JSON in {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python format_converter.py <input_file> <output_file>")
        sys.exit(1)
    convert_json(sys.argv[1], sys.argv[2])