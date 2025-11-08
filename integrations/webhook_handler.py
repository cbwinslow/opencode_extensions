#!/usr/bin/env python3

import json
import sys
import urllib.request

def handle_github_webhook(payload):
    # Example: create issue
    url = "https://api.github.com/repos/owner/repo/issues"
    headers = {"Authorization": "token YOUR_TOKEN", "Accept": "application/vnd.github.v3+json"}
    data = json.dumps({"title": "Webhook Issue", "body": str(payload)}).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req) as response:
        print("GitHub issue created")

def handle_gitlab_webhook(payload):
    # Example: create issue
    url = "https://gitlab.com/api/v4/projects/123/issues"
    headers = {"Private-Token": "YOUR_TOKEN"}
    data = json.dumps({"title": "Webhook Issue", "description": str(payload)}).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req) as response:
        print("GitLab issue created")

def handle_linear_webhook(payload):
    # Example: create issue
    url = "https://api.linear.app/issues"
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    data = json.dumps({"title": "Webhook Issue", "description": str(payload)}).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req) as response:
        print("Linear issue created")

if __name__ == "__main__":
    payload = json.load(sys.stdin)
    platform = sys.argv[1] if len(sys.argv) > 1 else "github"
    if platform == "github":
        handle_github_webhook(payload)
    elif platform == "gitlab":
        handle_gitlab_webhook(payload)
    elif platform == "linear":
        handle_linear_webhook(payload)