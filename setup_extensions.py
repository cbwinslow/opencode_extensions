#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from pathlib import Path

class OpenCodeExtensionManager:
    def __init__(self):
        self.extensions_dir = Path("extensions")
        self.config_dir = Path("extension_configs")
        self.config_dir.mkdir(exist_ok=True)
    
    def setup_opencode_mcp_tool(self):
        """Setup opencode MCP tool integration"""
        print("🔧 Setting up OpenCode MCP Tool...")
        
        # Read package.json to understand dependencies
        package_json_path = self.extensions_dir / "opencode-mcp-tool" / "package.json"
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            print(f"   📦 Package: {package_data.get('name', 'opencode-mcp-tool')}")
            print(f"   📋 Version: {package_data.get('version', 'unknown')}")
            
            # Create integration config
            config = {
                "name": "opencode-mcp-tool",
                "description": "MCP server for interacting with opencode CLI tool",
                "installation": "npx -y opencode-mcp-tool",
                "features": [
                    "Multi-model support via OpenCode",
                    "Plan mode for structured analysis",
                    "Model selection (primary + fallback)",
                    "Slash commands (/plan, /build, /help, /ping)",
                    "Brainstorming capabilities"
                ],
                "setup_commands": [
                    "claude mcp add opencode -- npx -y opencode-mcp-tool",
                    "claude mcp list"
                ],
                "verification": "Type /mcp in Claude Code to verify"
            }
            
            with open(self.config_dir / "opencode_mcp_config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            print("   ✅ Configuration saved")
            return True
        
        return False
    
    def setup_ai_sessions_mcp(self):
        """Setup AI sessions MCP server"""
        print("🔧 Setting up AI Sessions MCP...")
        
        # Check if binary exists or needs building
        ai_sessions_dir = self.extensions_dir / "ai-sessions-mcp"
        if ai_sessions_dir.exists():
            # Try to build if Go is available
            try:
                result = subprocess.run(['go', 'version'], capture_output=True, text=True)
                if result.returncode == 0:
                    print("   🔨 Building AI Sessions MCP...")
                    build_result = subprocess.run([
                        'go', 'build', '-o', 'bin/aisessions', './cmd/ai-sessions'
                    ], cwd=ai_sessions_dir, capture_output=True, text=True)
                    
                    if build_result.returncode == 0:
                        print("   ✅ Build successful")
                    else:
                        print(f"   ⚠️  Build failed: {build_result.stderr}")
                else:
                    print("   ⚠️  Go not found, skipping build")
            except FileNotFoundError:
                print("   ⚠️  Go not found, skipping build")
            
            config = {
                "name": "ai-sessions-mcp",
                "description": "MCP server for searching AI coding sessions",
                "features": [
                    "Session search across Claude Code, Gemini CLI, opencode",
                    "BM25 ranking for relevance-based search",
                    "Contextual snippets with search results",
                    "Pagination support for large sessions",
                    "Upload functionality for aisessions.dev"
                ],
                "installation_options": [
                    "curl -fsSL https://aisessions.dev/install.sh | bash",
                    "Download from GitHub releases",
                    "Build from source with Go"
                ],
                "usage": "Search previous coding sessions across multiple AI tools"
            }
            
            with open(self.config_dir / "ai_sessions_config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            print("   ✅ Configuration saved")
            return True
        
        return False
    
    def setup_llms_system(self):
        """Setup LLMs configuration management system"""
        print("🔧 Setting up LLMs Configuration System...")
        
        llms_dir = self.extensions_dir / "llms"
        if llms_dir.exists():
            # Check if it's a Python package
            setup_py = llms_dir / "setup.py"
            pyproject = llms_dir / "pyproject.toml"
            
            if setup_py.exists() or pyproject.exists():
                print("   🐍 Python package detected")
                
                # Install dependencies if possible
                try:
                    requirements = llms_dir / "requirements.txt"
                    if requirements.exists():
                        print("   📦 Installing dependencies...")
                        result = subprocess.run([
                            'pip3', 'install', '-r', str(requirements)
                        ], capture_output=True, text=True)
                        
                        if result.returncode == 0:
                            print("   ✅ Dependencies installed")
                        else:
                            print(f"   ⚠️  Install failed: {result.stderr}")
                except Exception as e:
                    print(f"   ⚠️  Could not install dependencies: {e}")
            
            config = {
                "name": "llms",
                "description": "Centralized LLM configuration and documentation management",
                "features": [
                    "Feature-Implementer v2 Architecture (14 specialized agents)",
                    "Scope Intelligence System (Global/Project/Local configs)",
                    "Documentation fetcher for multiple LLM providers",
                    "Skill/Command/Agent/Prompt builders",
                    "MCP server management",
                    "Plugin builder for distribution",
                    "Hook configuration with quality gates",
                    "FOSS-first policy"
                ],
                "components": [
                    "Agent Builder",
                    "Skill Builder", 
                    "Command Builder",
                    "Prompt Builder",
                    "Plugin Builder",
                    "MCP Manager",
                    "Documentation Fetcher",
                    "Scope Manager"
                ],
                "status": "Production Ready v1.0.0"
            }
            
            with open(self.config_dir / "llms_config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            print("   ✅ Configuration saved")
            return True
        
        return False
    
    def setup_systemprompt_orchestrator(self):
        """Setup SystemPrompt Code Orchestrator"""
        print("🔧 Setting up SystemPrompt Code Orchestrator...")
        
        orchestrator_dir = self.extensions_dir / "systemprompt-code-orchestrator"
        if orchestrator_dir.exists():
            package_json = orchestrator_dir / "package.json"
            if package_json.exists():
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                
                print(f"   📦 Package: {package_data.get('name', 'systemprompt-code-orchestrator')}")
                
                config = {
                    "name": "systemprompt-code-orchestrator",
                    "description": "AI coding agent orchestration for Claude Code, Gemini CLI, opencode",
                    "features": [
                        "Task management and process execution",
                        "Git integration",
                        "Multi-agent coordination",
                        "Workflow automation",
                        "Code generation and review"
                    ],
                    "installation": "npm install systemprompt-code-orchestrator",
                    "compatibility": ["Claude Code", "Gemini CLI", "opencode"]
                }
                
                with open(self.config_dir / "systemprompt_config.json", 'w') as f:
                    json.dump(config, f, indent=2)
                
                print("   ✅ Configuration saved")
                return True
        
        return False
    
    def setup_fastmcp(self):
        """Setup FastMCP framework"""
        print("🔧 Setting up FastMCP Framework...")
        
        fastmcp_dir = self.extensions_dir / "fastmcp"
        if fastmcp_dir.exists():
            config = {
                "name": "fastmcp",
                "description": "High-level framework for building MCP servers",
                "features": [
                    "Rapid MCP server development",
                    "Python-based framework",
                    "Simplified API",
                    "Template generation",
                    "Testing utilities"
                ],
                "usage": "Build custom MCP servers for opencode extensions",
                "installation": "pip install fastmcp"
            }
            
            with open(self.config_dir / "fastmcp_config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            print("   ✅ Configuration saved")
            return True
        
        return False
    
    def setup_mcp_box(self):
        """Setup MCP-Box management tool"""
        print("🔧 Setting up MCP-Box...")
        
        mcp_box_dir = self.extensions_dir / "mcp-box"
        if mcp_box_dir.exists():
            package_json = mcp_box_dir / "package.json"
            if package_json.exists():
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                
                print(f"   📦 Package: {package_data.get('name', 'mcp-box')}")
                
                config = {
                    "name": "mcp-box",
                    "description": "Universal MCP CLI tool for server management",
                    "features": [
                        "Server discovery and installation",
                        "Configuration management",
                        "Registry integration",
                        "Security validation",
                        "Multi-platform support"
                    ],
                    "installation": "npm install mcp-box",
                    "commands": [
                        "mcp-box init",
                        "mcp-box install <server>",
                        "mcp-box list",
                        "mcp-box configure"
                    ]
                }
                
                with open(self.config_dir / "mcp_box_config.json", 'w') as f:
                    json.dump(config, f, indent=2)
                
                print("   ✅ Configuration saved")
                return True
        
        return False
    
    def create_integration_summary(self):
        """Create summary of all integrations"""
        print("\n📋 Creating Integration Summary...")
        
        summary = {
            "opencode_extensions": {
                "installed_at": str(subprocess.check_output(['date'], text=True).strip()),
                "total_extensions": 6,
                "extensions": {}
            }
        }
        
        # Load all configs
        for config_file in self.config_dir.glob("*_config.json"):
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                extension_name = config_data['name']
                summary["opencode_extensions"]["extensions"][extension_name] = {
                    "description": config_data['description'],
                    "features": config_data.get('features', []),
                    "status": "configured"
                }
        
        with open(self.config_dir / "integration_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("   ✅ Integration summary saved")
        return summary
    
    def setup_all_extensions(self):
        """Setup all downloaded extensions"""
        print("🚀 Setting up OpenCode Extensions")
        print("=" * 50)
        
        extensions_setup = []
        
        # Setup each extension
        if self.setup_opencode_mcp_tool():
            extensions_setup.append("opencode-mcp-tool")
        
        if self.setup_ai_sessions_mcp():
            extensions_setup.append("ai-sessions-mcp")
        
        if self.setup_llms_system():
            extensions_setup.append("llms")
        
        if self.setup_systemprompt_orchestrator():
            extensions_setup.append("systemprompt-code-orchestrator")
        
        if self.setup_fastmcp():
            extensions_setup.append("fastmcp")
        
        if self.setup_mcp_box():
            extensions_setup.append("mcp-box")
        
        # Create summary
        summary = self.create_integration_summary()
        
        print(f"\n✅ Setup Complete!")
        print(f"📊 Extensions configured: {len(extensions_setup)}")
        print(f"📁 Configurations saved in: {self.config_dir}")
        
        print(f"\n🔧 Quick Start Commands:")
        print(f"   # OpenCode MCP Tool:")
        print(f"   claude mcp add opencode -- npx -y opencode-mcp-tool")
        print(f"   ")
        print(f"   # AI Sessions:")
        print(f"   curl -fsSL https://aisessions.dev/install.sh | bash")
        print(f"   ")
        print(f"   # MCP Management:")
        print(f"   npm install mcp-box")
        print(f"   mcp-box init")
        
        return summary

if __name__ == "__main__":
    manager = OpenCodeExtensionManager()
    manager.setup_all_extensions()