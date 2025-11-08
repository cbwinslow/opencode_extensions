#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

class FilesystemMCPServer:
    def __init__(self):
        self.base_paths = [
            "/home/cbwinslow/opencode_extensions",
            "/home/cbwinslow/Downloads",
            "/home/cbwinslow/Documents"
        ]
    
    def list_files(self, path="."):
        """List files in directory"""
        results = []
        for base_path in self.base_paths:
            full_path = Path(base_path) / path
            if full_path.exists() and full_path.is_dir():
                try:
                    for item in full_path.iterdir():
                        results.append({
                            "name": item.name,
                            "path": str(item),
                            "type": "directory" if item.is_dir() else "file",
                            "size": item.stat().st_size if item.is_file() else 0
                        })
                except PermissionError:
                    continue
        return results
    
    def read_file(self, path):
        """Read file content"""
        for base_path in self.base_paths:
            full_path = Path(base_path) / path
            if full_path.exists() and full_path.is_file():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    return f"Error reading file: {e}"
        return "File not found"
    
    def handle_request(self, request):
        """Handle MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "list_files":
            return {"result": self.list_files(params.get("path", "."))}
        elif method == "read_file":
            return {"result": {"content": self.read_file(params.get("path"))}}
        else:
            return {"error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    server = FilesystemMCPServer()
    
    # Simple command line interface
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "list":
            path = sys.argv[2] if len(sys.argv) > 2 else "."
            result = server.list_files(path)
            print(json.dumps(result, indent=2))
        elif command == "read":
            path = sys.argv[2]
            result = server.read_file(path)
            print(result)
