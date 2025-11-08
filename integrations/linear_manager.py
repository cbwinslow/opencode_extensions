#!/usr/bin/env python3

import json
import subprocess
import sys
import urllib.request

def get_linear_token():
    # Retrieve from Bitwarden
    result = subprocess.run(["bw", "get", "password", "linear_token"], capture_output=True, text=True)
    return result.stdout.strip()

def create_linear_item(item_type, data, token):
    url = f"https://api.linear.app/{item_type}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = json.dumps(data).encode()
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def edit_linear_item(item_type, item_id, data, token):
    url = f"https://api.linear.app/{item_type}/{item_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = json.dumps(data).encode()
    req = urllib.request.Request(url, data=payload, headers=headers, method="PATCH")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def close_linear_item(item_type, item_id, token):
    return edit_linear_item(item_type, item_id, {"state": "done"}, token)

# Example usage for different item types
item_types = ["customers", "members", "documents", "conversations", "pulse"]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python linear_manager.py <action> <item_type> [args...]")
        sys.exit(1)
    action = sys.argv[1]
    item_type = sys.argv[2]
    token = get_linear_token()
    if action == "create":
        # Assume additional args for data
        data = {"name": sys.argv[3], "description": sys.argv[4] if len(sys.argv) > 4 else ""}
        result = create_linear_item(item_type, data, token)
        print(json.dumps(result, indent=2))
    elif action == "edit":
        item_id = sys.argv[3]
        data = {"name": sys.argv[4]}
        result = edit_linear_item(item_type, item_id, data, token)
        print(json.dumps(result, indent=2))
    elif action == "close":
        item_id = sys.argv[3]
        result = close_linear_item(item_type, item_id, token)
        print(json.dumps(result, indent=2))