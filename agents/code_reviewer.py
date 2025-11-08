#!/usr/bin/env python3

import sys
import os
import subprocess

def review_code(file_path):
    issues = []
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if 'TODO' in line and 'TODO' not in issues:
                    issues.append(f"Line {i}: Found TODO comment - consider addressing or removing.")
                if 'FIXME' in line and 'FIXME' not in issues:
                    issues.append(f"Line {i}: Found FIXME comment - indicates known issue.")
                if len(line) > 100:
                    issues.append(f"Line {i}: Line too long ({len(line)} chars) - consider breaking up.")
    except Exception as e:
        issues.append(f"Error reading file: {e}")
    return issues

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python code_reviewer.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        sys.exit(1)
    issues = review_code(file_path)
    if issues:
        print("Code review issues found:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No issues found in code review.")