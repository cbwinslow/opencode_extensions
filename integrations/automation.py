#!/usr/bin/env python3

import json
import subprocess
import sys
import urllib.request

def get_token(source):
    # Placeholder for token retrieval from Bitwarden or Vault
    if source == "bitwarden":
        # Use bw CLI
        result = subprocess.run(["bw", "get", "password", "github_token"], capture_output=True, text=True)
        return result.stdout.strip()
    elif source == "vault":
        # Use vault CLI
        result = subprocess.run(["vault", "kv", "get", "-field=password", "secret/github_token"], capture_output=True, text=True)
        return result.stdout.strip()
    return None

def create_github_issue(repo, title, body, token):
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    data = json.dumps({"title": title, "body": body}).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def edit_github_issue(repo, issue_number, title, body, token):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    data = json.dumps({"title": title, "body": body}).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def close_github_issue(repo, issue_number, token):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    data = json.dumps({"state": "closed"}).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

# Similar functions for GitLab and Linear can be added here

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python automation.py <action> [args...]")
        sys.exit(1)
    action = sys.argv[1]
    if action == "create_issue":
        repo = sys.argv[2]
        title = sys.argv[3]
        body = sys.argv[4]
        token = get_token("bitwarden")
        result = create_github_issue(repo, title, body, token)
        print(json.dumps(result, indent=2))
    elif action == "edit_issue":
        repo = sys.argv[2]
        number = sys.argv[3]
        title = sys.argv[4]
        body = sys.argv[5]
        token = get_token("bitwarden")
        result = edit_github_issue(repo, number, title, body, token)
        print(json.dumps(result, indent=2))
    elif action == "close_issue":
        repo = sys.argv[2]
        number = sys.argv[3]
        token = get_token("bitwarden")
        result = close_github_issue(repo, number, token)
        print(json.dumps(result, indent=2))