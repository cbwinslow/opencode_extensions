#!/usr/bin/env python3

import subprocess
import sys
import os

def get_token_from_bitwarden(item_name):
    try:
        result = subprocess.run(["bw", "get", "password", item_name], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Failed to retrieve {item_name} from Bitwarden")
        return None

def get_token_from_vault(path, field="password"):
    try:
        result = subprocess.run(["vault", "kv", "get", f"-field={field}", path], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Failed to retrieve token from Vault at {path}")
        return None

def authenticate_ssh(key_path):
    try:
        # Assume key is unlocked or use ssh-agent
        result = subprocess.run(["ssh", "-i", key_path, "user@host", "echo", "authenticated"], capture_output=True, text=True, check=True)
        return "authenticated" in result.stdout
    except subprocess.CalledProcessError:
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python token_manager.py <source> [args...]")
        sys.exit(1)
    source = sys.argv[1]
    if source == "bitwarden":
        item = sys.argv[2]
        token = get_token_from_bitwarden(item)
        if token:
            print(f"Token: {token}")
    elif source == "vault":
        path = sys.argv[2]
        field = sys.argv[3] if len(sys.argv) > 3 else "password"
        token = get_token_from_vault(path, field)
        if token:
            print(f"Token: {token}")
    elif source == "ssh":
        key_path = sys.argv[2]
        if authenticate_ssh(key_path):
            print("SSH authentication successful")
        else:
            print("SSH authentication failed")