#!/usr/bin/env python3

import os
import subprocess
import glob

def find_tests(directory='.'):
    test_files = []
    for ext in ['test_*.py', '*_test.py', 'test_*.js', '*_test.js']:
        test_files.extend(glob.glob(os.path.join(directory, '**', ext), recursive=True))
    return test_files

def run_tests(test_files):
    results = []
    for test_file in test_files:
        try:
            if test_file.endswith('.py'):
                result = subprocess.run(['python', '-m', 'pytest', test_file], capture_output=True, text=True)
            elif test_file.endswith('.js'):
                result = subprocess.run(['npm', 'test', '--', test_file], capture_output=True, text=True)
            else:
                results.append(f"Unsupported test file: {test_file}")
                continue
            if result.returncode == 0:
                results.append(f"PASSED: {test_file}")
            else:
                results.append(f"FAILED: {test_file} - {result.stdout} {result.stderr}")
        except Exception as e:
            results.append(f"ERROR running {test_file}: {e}")
    return results

if __name__ == "__main__":
    tests = find_tests()
    if not tests:
        print("No test files found.")
    else:
        print(f"Found {len(tests)} test files. Running tests...")
        results = run_tests(tests)
        for result in results:
            print(result)