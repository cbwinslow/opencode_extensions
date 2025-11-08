#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

def demo_extensions():
    """Demonstrate the downloaded OpenCode extensions"""
    print("🚀 OpenCode Extensions Demo")
    print("=" * 60)
    print("6 Powerful Extensions for Enhanced AI Coding")
    print("=" * 60)
    
    # Load integration summary
    config_dir = Path("extension_configs")
    summary_file = config_dir / "integration_summary.json"
    
    if summary_file.exists():
        with open(summary_file, 'r') as f:
            summary = json.load(f)
        
        extensions = summary["opencode_extensions"]["extensions"]
        total = summary["opencode_extensions"]["total_extensions"]
        
        print(f"\n📊 Extensions Overview: {total} extensions configured")
        print()
        
        # Demo each extension
        for i, (name, info) in enumerate(extensions.items(), 1):
            print(f"{i}. 📦 {name}")
            print(f"   📋 {info['description']}")
            print(f"   ✨ Features: {len(info['features'])} features")
            print(f"   📌 Status: {info['status']}")
            
            # Show key features
            for feature in info['features'][:3]:  # Show first 3 features
                print(f"      • {feature}")
            
            if len(info['features']) > 3:
                print(f"      • ... and {len(info['features']) - 3} more")
            
            print()
    
    # Show practical workflows
    print("🎯 Practical Workflows:")
    print()
    
    workflows = [
        {
            "name": "Multi-Model Code Analysis",
            "extensions": ["opencode-mcp-tool", "ai-sessions-mcp"],
            "description": "Use multiple AI models to analyze code and find similar past solutions"
        },
        {
            "name": "Agent-Based Development",
            "extensions": ["llms", "systemprompt-code-orchestrator"],
            "description": "Coordinate specialized agents for complex development tasks"
        },
        {
            "name": "Custom Tool Development",
            "extensions": ["fastmcp", "mcp-box"],
            "description": "Build and manage custom MCP servers for specific needs"
        },
        {
            "name": "Knowledge Management",
            "extensions": ["ai-sessions-mcp", "llms"],
            "description": "Organize and search across all AI coding sessions and documentation"
        }
    ]
    
    for workflow in workflows:
        print(f"🔧 {workflow['name']}")
        print(f"   📚 Uses: {', '.join(workflow['extensions'])}")
        print(f"   💡 {workflow['description']}")
        print()
    
    # Show integration with existing tools
    print("🔗 Integration with Existing OpenCode Features:")
    print()
    
    integrations = [
        "🧠 Hierarchical Memory: Store session findings and concepts",
        "🔐 FOSS Token Manager: Secure credentials for all extensions", 
        "🔍 Code Analyzer: Analyze extension code and patterns",
        "🏗️ Project Manager: Create projects with extension templates",
        "📊 Memory Config: Configure memory for extension data"
    ]
    
    for integration in integrations:
        print(f"   {integration}")
    
    # Show cost savings
    print(f"\n💰 Value Proposition:")
    print(f"   🆓 All extensions: 100% Free and Open Source")
    print(f"   🏠 Self-hosted: Complete data control")
    print(f"   🔄 No vendor lock-in: Use with any AI tool")
    print(f"   🌍 Community-driven: Regular updates and improvements")
    
    # Show quick start commands
    print(f"\n🚀 Quick Start:")
    print()
    
    commands = [
        ("OpenCode MCP Tool", "claude mcp add opencode -- npx -y opencode-mcp-tool"),
        ("AI Sessions", "curl -fsSL https://aisessions.dev/install.sh | bash"),
        ("MCP Management", "npm install mcp-box && mcp-box init"),
        ("Custom MCP Server", "pip install fastmcp && fastmcp create my-tool"),
        ("LLM Configuration", "cd extensions/llms && pip install -r requirements.txt")
    ]
    
    for name, command in commands:
        print(f"   📦 {name}:")
        print(f"      {command}")
        print()
    
    # Show file structure
    print("📁 Extension Structure:")
    print()
    
    extensions_dir = Path("extensions")
    if extensions_dir.exists():
        for item in extensions_dir.iterdir():
            if item.is_dir():
                # Count files
                file_count = len(list(item.rglob("*")))
                print(f"   📂 extensions/{item.name}/ ({file_count} files)")
    
    print(f"\n📚 Documentation:")
    print(f"   📖 Full Guide: EXTENSIONS_GUIDE.md")
    print(f"   🧠 Memory System: HIERARCHICAL_MEMORY.md") 
    print(f"   🌟 FOSS Alternatives: FOSS_ALTERNATIVES.md")
    print(f"   🤖 Agent Guidelines: AGENTS.md")
    
    print(f"\n✨ Demo Complete!")
    print(f"🎯 Your OpenCode setup is now supercharged with 6 powerful extensions!")
    print(f"🌟 All 100% FOSS and ready to use!")

if __name__ == "__main__":
    demo_extensions()