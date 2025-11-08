#!/usr/bin/env python3

import json
import subprocess
import sys
import os
from pathlib import Path

class MCPServerManager:
    def __init__(self):
        self.settings_path = self.find_mcp_settings()
        self.mcp_servers = {}
        self.download_dir = Path("mcp_servers_downloaded")
        self.download_dir.mkdir(exist_ok=True)
    
    def find_mcp_settings(self):
        """Find MCP settings file"""
        possible_paths = [
            "/home/cbwinslow/config/Development/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json",
            "/home/cbwinslow/.config/claude/settings.json",
            "/home/cbwinslow/.config/claude-desktop/settings.json",
            "./mcp_settings.json"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                print(f"📁 Found MCP settings at: {path}")
                return path
        
        # Create local settings if none found
        print("📝 Creating local MCP settings file")
        return "./mcp_settings.json"
    
    def load_current_settings(self):
        """Load current MCP settings"""
        if Path(self.settings_path).exists():
            with open(self.settings_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("⚠️  Invalid JSON in settings file")
                    return {"mcpServers": {}}
        return {"mcpServers": {}}
    
    def get_mcp_server_list(self):
        """Get comprehensive list of MCP servers"""
        return {
            # Core Productivity Servers
            "filesystem": {
                "package": "@modelcontextprotocol/server-filesystem",
                "description": "File system access and operations",
                "category": "core",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/cbwinslow/opencode_extensions", "/home/cbwinslow/Downloads"],
                "env": {}
            },
            "memory": {
                "package": "@modelcontextprotocol/server-memory",
                "description": "Persistent memory for conversations",
                "category": "core",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-memory"],
                "env": {}
            },
            "fetch": {
                "package": "@modelcontextprotocol/server-fetch",
                "description": "HTTP requests and web scraping",
                "category": "core",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-fetch"],
                "env": {}
            },
            
            # Development Tools
            "git": {
                "package": "mcp-server-git",
                "description": "Git repository operations",
                "category": "development",
                "install": "uvx",
                "args": ["mcp-server-git", "--repository", "/home/cbwinslow/opencode_extensions"],
                "env": {}
            },
            "github": {
                "package": "@modelcontextprotocol/server-github",
                "description": "GitHub API integration",
                "category": "development",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": ""}
            },
            "python": {
                "package": "mcp-server-python",
                "description": "Python code execution",
                "category": "development",
                "install": "uvx",
                "args": ["mcp-server-python"],
                "env": {}
            },
            
            # Database Servers
            "sqlite": {
                "package": "@modelcontextprotocol/server-sqlite",
                "description": "SQLite database access",
                "category": "database",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sqlite", "/home/cbwinslow/opencode_extensions/hierarchical_memory.db"],
                "env": {}
            },
            "postgres": {
                "package": "@modelcontextprotocol/server-postgres",
                "description": "PostgreSQL database access",
                "category": "database",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-postgres"],
                "env": {"POSTGRES_CONNECTION_STRING": "postgresql://username:password@localhost:5432/database"}
            },
            
            # Web & Automation
            "puppeteer": {
                "package": "@modelcontextprotocol/server-puppeteer",
                "description": "Web browser automation",
                "category": "web",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
                "env": {},
                "alwaysAllow": ["puppeteer_navigate", "puppeteer_screenshot", "puppeteer_click"]
            },
            "brave-search": {
                "package": "@modelcontextprotocol/server-brave-search",
                "description": "Brave search API integration",
                "category": "web",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                "env": {"BRAVE_API_KEY": ""}
            },
            "tavily": {
                "package": "@modelcontextprotocol/server-tavily",
                "description": "Tavily search API integration",
                "category": "web",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-tavily"],
                "env": {"TAVILY_API_KEY": ""}
            },
            
            # Cloud & Infrastructure
            "docker": {
                "package": "@modelcontextprotocol/server-docker",
                "description": "Docker container management",
                "category": "infrastructure",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-docker"],
                "env": {}
            },
            "kubernetes": {
                "package": "@modelcontextprotocol/server-kubernetes",
                "description": "Kubernetes cluster management",
                "category": "infrastructure",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-kubernetes"],
                "env": {}
            },
            "aws": {
                "package": "@modelcontextprotocol/server-aws",
                "description": "AWS services integration",
                "category": "infrastructure",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-aws"],
                "env": {"AWS_ACCESS_KEY_ID": "", "AWS_SECRET_ACCESS_KEY": "", "AWS_DEFAULT_REGION": "us-west-2"}
            },
            
            # Third-party Integrations
            "slack": {
                "package": "@modelcontextprotocol/server-slack",
                "description": "Slack workspace integration",
                "category": "integration",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-slack"],
                "env": {"SLACK_BOT_TOKEN": "", "SLACK_APP_TOKEN": ""}
            },
            "gdrive": {
                "package": "@modelcontextprotocol/server-gdrive",
                "description": "Google Drive integration",
                "category": "integration",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-gdrive"],
                "env": {"GOOGLE_CLIENT_ID": "", "GOOGLE_CLIENT_SECRET": "", "GOOGLE_REDIRECT_URI": ""}
            },
            
            # AI & Creative
            "everart": {
                "package": "@modelcontextprotocol/server-everart",
                "description": "EverArt AI image generation",
                "category": "ai",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-everart"],
                "env": {"EVERART_API_KEY": ""}
            },
            "sequentialthinking": {
                "package": "@modelcontextprotocol/server-sequential-thinking",
                "description": "Sequential thinking and reasoning",
                "category": "ai",
                "install": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
                "env": {}
            },
            "context7": {
                "package": "@upstash/context7-mcp",
                "description": "Context management and retrieval",
                "category": "ai",
                "install": "npx",
                "args": ["-y", "@upstash/context7-mcp"],
                "env": {"DEFAULT_MINIMUM_TOKENS": ""}
            },
            
            # OpenCode Extensions
            "opencode-mcp-tool": {
                "package": "opencode-mcp-tool",
                "description": "OpenCode CLI integration",
                "category": "opencode",
                "install": "npx",
                "args": ["-y", "opencode-mcp-tool"],
                "env": {}
            }
        }
    
    def check_installation_method(self, method):
        """Check if installation method is available"""
        if method == "npx":
            try:
                result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
                return result.returncode == 0
            except FileNotFoundError:
                return False
        elif method == "uvx":
            try:
                result = subprocess.run(['uvx', '--version'], capture_output=True, text=True)
                return result.returncode == 0
            except FileNotFoundError:
                return False
        return False
    
    def install_mcp_server(self, server_name, server_config):
        """Install a specific MCP server"""
        print(f"📦 Installing {server_name}...")
        
        install_method = server_config["install"]
        package = server_config["package"]
        
        if not self.check_installation_method(install_method):
            print(f"   ⚠️  {install_method} not available, skipping {server_name}")
            return False
        
        try:
            if install_method == "npx":
                # Test if package is available
                result = subprocess.run([
                    'npx', '-y', package, '--help'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"   ✅ {server_name} is available")
                    return True
                else:
                    print(f"   ⚠️  {server_name} installation test failed")
                    return False
                    
            elif install_method == "uvx":
                result = subprocess.run([
                    'uvx', '--help'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"   ✅ {server_name} is available via uvx")
                    return True
                else:
                    print(f"   ⚠️  {server_name} installation test failed")
                    return False
                    
        except subprocess.TimeoutExpired:
            print(f"   ⏰ {server_name} installation timed out")
            return False
        except Exception as e:
            print(f"   ❌ {server_name} installation failed: {e}")
            return False
    
    def create_mcp_settings(self, selected_servers=None):
        """Create MCP settings file"""
        all_servers = self.get_mcp_server_list()
        current_settings = self.load_current_settings()
        
        if selected_servers is None:
            # Default to core and development servers
            selected_servers = [
                "filesystem", "memory", "fetch", "git", "python", 
                "sqlite", "opencode-mcp-tool", "sequentialthinking"
            ]
        
        mcp_servers = {}
        
        for server_name in selected_servers:
            if server_name in all_servers:
                server_config = all_servers[server_name]
                
                # Build server configuration
                server_entry = {
                    "command": server_config["install"],
                    "args": server_config["args"],
                    "env": server_config.get("env", {})
                }
                
                # Add alwaysAllow if present
                if "alwaysAllow" in server_config:
                    server_entry["alwaysAllow"] = server_config["alwaysAllow"]
                
                mcp_servers[server_name] = server_entry
                
                # Try to install the server
                self.install_mcp_server(server_name, server_config)
        
        # Update settings
        current_settings["mcpServers"] = mcp_servers
        
        # Save to both original location and local
        settings_files = [self.settings_path, "./mcp_settings.json"]
        
        for settings_file in settings_files:
            with open(settings_file, 'w') as f:
                json.dump(current_settings, f, indent=2)
            print(f"   💾 Settings saved to {settings_file}")
        
        return current_settings
    
    def list_available_servers(self):
        """List all available MCP servers by category"""
        all_servers = self.get_mcp_server_list()
        categories = {}
        
        for name, config in all_servers.items():
            category = config["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((name, config["description"]))
        
        print("📋 Available MCP Servers by Category:")
        print("=" * 50)
        
        for category, servers in categories.items():
            print(f"\n🏷️  {category.title()}:")
            for name, description in servers:
                print(f"   📦 {name}: {description}")
    
    def test_mcp_servers(self):
        """Test installed MCP servers"""
        current_settings = self.load_current_settings()
        mcp_servers = current_settings.get("mcpServers", {})
        
        print("🧪 Testing MCP Servers:")
        print("=" * 30)
        
        for server_name, server_config in mcp_servers.items():
            print(f"\n🔍 Testing {server_name}:")
            
            command = server_config["command"]
            args = server_config.get("args", [])
            
            try:
                if command == "npx" and args:
                    # Test with --help flag
                    test_args = args.copy()
                    if "--help" not in test_args:
                        test_args.append("--help")
                    
                    result = subprocess.run(
                        [command] + test_args,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        print("   ✅ Server is accessible")
                    else:
                        print("   ⚠️  Server test failed")
                        
                elif command == "uvx":
                    result = subprocess.run(
                        [command, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        print("   ✅ uvx is available")
                    else:
                        print("   ⚠️  uvx test failed")
                        
            except Exception as e:
                print(f"   ❌ Test failed: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python mcp_manager.py <command> [args...]")
        print("Commands:")
        print("  list                    - List available MCP servers")
        print("  install [servers...]     - Install specific servers (default: core servers)")
        print("  test                    - Test installed servers")
        print("  setup                   - Interactive setup")
        sys.exit(1)
    
    command = sys.argv[1]
    manager = MCPServerManager()
    
    if command == "list":
        manager.list_available_servers()
    
    elif command == "install":
        servers = sys.argv[2:] if len(sys.argv) > 2 else None
        manager.create_mcp_settings(servers)
    
    elif command == "test":
        manager.test_mcp_servers()
    
    elif command == "setup":
        print("🚀 Interactive MCP Server Setup")
        print("Select servers to install (comma-separated):")
        manager.list_available_servers()
        print("\nExample: filesystem,memory,git,github")
        
        selection = input("\nEnter servers: ").strip()
        if selection:
            selected = [s.strip() for s in selection.split(',')]
            manager.create_mcp_settings(selected)
        else:
            print("Using default core servers...")
            manager.create_mcp_settings()
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()