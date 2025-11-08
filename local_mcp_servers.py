#!/usr/bin/env python3

import json
import sqlite3
import subprocess
import sys
import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

class LocalMCPServer:
    """Create local MCP servers that don't require npm/uvx"""
    
    def __init__(self):
        self.servers_dir = Path("local_mcp_servers")
        self.servers_dir.mkdir(exist_ok=True)
        self.db_path = "hierarchical_memory.db"
    
    def create_filesystem_server(self):
        """Create a simple filesystem MCP server"""
        server_code = '''#!/usr/bin/env python3
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
'''
        
        with open(self.servers_dir / "filesystem_server.py", 'w') as f:
            f.write(server_code)
        os.chmod(self.servers_dir / "filesystem_server.py", 0o755)
    
    def create_memory_server(self):
        """Create a memory MCP server using our hierarchical memory"""
        server_code = '''#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
exec(open('tools/hierarchical_memory.py').read())

class MemoryMCPServer:
    def __init__(self):
        self.memory = HierarchicalMemoryManager()
    
    def handle_request(self, request):
        """Handle MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        
        try:
            if method == "create_session":
                title = params.get("title", "New Session")
                session_id = self.memory.create_session(title)
                return {"result": {"session_id": session_id}}
            
            elif method == "add_conversation":
                session_id = params.get("session_id")
                role = params.get("role")
                content = params.get("content")
                node_id = self.memory.add_conversation_turn(session_id, role, content)
                return {"result": {"node_id": node_id}}
            
            elif method == "search_by_tag":
                tag = params.get("tag")
                results = self.memory.search_by_tag(tag)
                return {"result": results}
            
            elif method == "get_hierarchy":
                node_id = params.get("node_id")
                hierarchy = self.memory.get_node_hierarchy(node_id)
                return {"result": hierarchy}
            
            else:
                return {"error": {"code": -32601, "message": "Method not found"}}
        
        except Exception as e:
            return {"error": {"code": -32603, "message": str(e)}}

if __name__ == "__main__":
    server = MemoryMCPServer()
    
    # Simple command line interface
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create_session":
            title = sys.argv[2] if len(sys.argv) > 2 else "New Session"
            result = server.memory.create_session(title)
            print(f"Session created: {result}")
        
        elif command == "add_conversation":
            if len(sys.argv) >= 4:
                session_id = sys.argv[2]
                role = sys.argv[3]
                content = ' '.join(sys.argv[4:])
                result = server.memory.add_conversation_turn(session_id, role, content)
                print(f"Conversation added: {result}")
        
        elif command == "search":
            tag = sys.argv[2] if len(sys.argv) > 2 else "python"
            results = server.memory.search_by_tag(tag)
            print(json.dumps(results, indent=2))
'''
        
        with open(self.servers_dir / "memory_server.py", 'w') as f:
            f.write(server_code)
        os.chmod(self.servers_dir / "memory_server.py", 0o755)
    
    def create_git_server(self):
        """Create a Git MCP server"""
        server_code = '''#!/usr/bin/env python3
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
'''
        
        with open(self.servers_dir / "git_server.py", 'w') as f:
            f.write(server_code)
        os.chmod(self.servers_dir / "git_server.py", 0o755)
    
    def create_all_servers(self):
        """Create all local MCP servers"""
        print("🔧 Creating local MCP servers...")
        
        self.create_filesystem_server()
        print("   ✅ Filesystem server created")
        
        self.create_memory_server()
        print("   ✅ Memory server created")
        
        self.create_git_server()
        print("   ✅ Git server created")
        
        print(f"   📁 Servers created in: {self.servers_dir}")
    
    def create_settings_with_local_servers(self):
        """Create settings.json with local servers"""
        settings = {
            "mcpServers": {
                "local-filesystem": {
                    "command": "python3",
                    "args": [str(self.servers_dir / "filesystem_server.py")],
                    "env": {}
                },
                "local-memory": {
                    "command": "python3", 
                    "args": [str(self.servers_dir / "memory_server.py")],
                    "env": {}
                },
                "local-git": {
                    "command": "python3",
                    "args": [str(self.servers_dir / "git_server.py")],
                    "env": {}
                }
            }
        }
        
        # Save settings
        with open("./mcp_settings_local.json", 'w') as f:
            json.dump(settings, f, indent=2)
        
        # Also update the main settings file
        main_settings_path = "/home/cbwinslow/config/Development/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json"
        
        try:
            with open(main_settings_path, 'r') as f:
                current_settings = json.load(f)
        except:
            current_settings = {"mcpServers": {}}
        
        # Add local servers to existing settings
        current_settings["mcpServers"].update(settings["mcpServers"])
        
        with open(main_settings_path, 'w') as f:
            json.dump(current_settings, f, indent=2)
        
        print("   💾 Settings updated with local servers")
        return settings

def main():
    if len(sys.argv) < 2:
        print("Usage: python local_mcp_servers.py <command>")
        print("Commands:")
        print("  create    - Create all local MCP servers")
        print("  setup     - Create servers and update settings")
        print("  test      - Test local servers")
        sys.exit(1)
    
    command = sys.argv[1]
    server_manager = LocalMCPServer()
    
    if command == "create":
        server_manager.create_all_servers()
    
    elif command == "setup":
        server_manager.create_all_servers()
        server_manager.create_settings_with_local_servers()
        print("\n✅ Local MCP servers setup complete!")
        print("🔄 Restart your AI assistant to use the new servers")
    
    elif command == "test":
        print("🧪 Testing local MCP servers...")
        
        # Test filesystem server
        try:
            result = subprocess.run([
                'python3', str(server_manager.servers_dir / "filesystem_server.py"), 'list'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("   ✅ Filesystem server working")
            else:
                print("   ❌ Filesystem server failed")
        except Exception as e:
            print(f"   ❌ Filesystem server error: {e}")
        
        # Test memory server
        try:
            result = subprocess.run([
                'python3', str(server_manager.servers_dir / "memory_server.py"), 'create_session', 'Test Session'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("   ✅ Memory server working")
            else:
                print("   ❌ Memory server failed")
        except Exception as e:
            print(f"   ❌ Memory server error: {e}")
        
        # Test git server
        try:
            result = subprocess.run([
                'python3', str(server_manager.servers_dir / "git_server.py"), 'status'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("   ✅ Git server working")
            else:
                print("   ❌ Git server failed")
        except Exception as e:
            print(f"   ❌ Git server error: {e}")

if __name__ == "__main__":
    main()