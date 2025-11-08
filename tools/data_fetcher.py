#!/usr/bin/env python3

import urllib.request
import json
import sys

def fetch_data(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python data_fetcher.py <url> [headers_json]")
        sys.exit(1)
    url = sys.argv[1]
    headers = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
    try:
        data = fetch_data(url, headers)
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error fetching data: {e}")