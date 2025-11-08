#!/usr/bin/env python3
import json
import sys
import subprocess
from pathlib import Path

class GitMCPServer:
    def __init__(self, repo_path="/home/cbwinslow/opencode_extensions"):
        self.repo_path = Path(repo_path)
    
    def run_git_command(self, args):
        """Run git command and return result"""
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_status(self):
        """Get git status"""
        return self.run_git_command(['status', '--porcelain'])
    
    def get_log(self, limit=10):
        """Get git log"""
        return self.run_git_command(['log', '--oneline', f'-{limit}'])
    
    def get_branches(self):
        """Get git branches"""
        return self.run_git_command(['branch', '-a'])
    
    def handle_request(self, request):
        """Handle MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "status":
            return {"result": self.get_status()}
        elif method == "log":
            limit = params.get("limit", 10)
            return {"result": self.get_log(limit)}
        elif method == "branches":
            return {"result": self.get_branches()}
        else:
            return {"error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    server = GitMCPServer()
    
    # Simple command line interface
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            result = server.get_status()
            print(json.dumps(result, indent=2))
        
        elif command == "log":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            result = server.get_log(limit)
            print(json.dumps(result, indent=2))
        
        elif command == "branches":
            result = server.get_branches()
            print(json.dumps(result, indent=2))
