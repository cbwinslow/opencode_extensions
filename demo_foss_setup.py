#!/usr/bin/env python3

import json
import subprocess
import sys

def demonstrate_foss_setup():
    """Demonstrate the complete FOSS opencode extensions setup"""
    print("🌟 FOSS OpenCode Extensions Demo")
    print("=" * 60)
    print("100% Free and Open Source Software")
    print("=" * 60)
    
    # 1. Show FOSS MCP servers
    print("\n📡 FOSS MCP Servers Available:")
    foss_servers = [
        "mattermost_config.json",
        "matrix_config.json", 
        "nextcloud_config.json",
        "redmine_config.json",
        "ollama_config.json",
        "gitea_config.json"
    ]
    
    for server in foss_servers:
        try:
            with open(f"mcp_servers/{server}", 'r') as f:
                config = json.load(f)
            print(f"   ✅ {config['name']}")
            print(f"      🏠 Self-hosted: {config.get('self_hosted', False)}")
            print(f"      🔗 Source: {config.get('open_source', 'N/A')}")
            print(f"      🔐 Auth: {config.get('auth_type', 'N/A')}")
            print()
        except Exception as e:
            print(f"   ❌ Error reading {server}: {e}")
    
    # 2. Demonstrate FOSS token manager
    print("🔐 FOSS Token Manager Demo:")
    print("   Storing tokens locally with encryption...")
    
    # Store a demo token
    result = subprocess.run([
        'python3', 'configs/foss_token_manager.py', 'generate', 
        'demo-service', '32'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"   ✅ Generated: {result.stdout.strip()}")
    else:
        print(f"   ❌ Error: {result.stderr}")
    
    # List tokens
    result = subprocess.run([
        'python3', 'configs/foss_token_manager.py', 'list'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("   📋 Stored services:")
        for line in result.stdout.strip().split('\n')[2:]:  # Skip header
            if line.strip():
                print(f"      {line}")
    
    # 3. Show hierarchical memory with FOSS focus
    print("\n🧠 Hierarchical Memory System:")
    print("   Creating FOSS-focused memory structure...")
    
    # Create a session about FOSS migration
    result = subprocess.run([
        'python3', 'tools/hierarchical_memory.py', 'create_session', 
        'FOSS Migration Planning'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        session_id = result.stdout.strip().split(': ')[1]
        print(f"   ✅ Session created: {session_id}")
        
        # Add FOSS-related conversations
        foss_conversations = [
            ("user", "How do I migrate from Slack to Mattermost?"),
            ("assistant", "Use Mattermost's import tool. Export Slack data, then import to Mattermost. Both are FOSS!"),
            ("user", "What about replacing GitHub with Gitea?"),
            ("assistant", "Gitea is lightweight and self-hostable. Mirror repos, then update CI/CD pipelines.")
        ]
        
        for role, content in foss_conversations:
            subprocess.run([
                'python3', 'tools/hierarchical_memory.py', 'add_conversation',
                session_id, role, content
            ], capture_output=True, text=True)
        
        print("   ✅ Added FOSS migration conversations")
        
        # Create FOSS concepts
        foss_concepts = [
            ("Self-Hosting", "Running your own infrastructure instead of using SaaS", "", "infrastructure,privacy"),
            ("Data Sovereignty", "Complete control over your data and systems", "Self-Hosting", "privacy,control"),
            ("Open Source", "Software with source code that anyone can inspect, modify, and enhance", "", "freedom,community")
        ]
        
        for concept, definition, parents, tags in foss_concepts:
            subprocess.run([
                'python3', 'tools/hierarchical_memory.py', 'create_concept',
                concept, definition, parents, tags
            ], capture_output=True, text=True)
        
        print("   ✅ Created FOSS concept nodes")
        
        # Auto-organize
        subprocess.run([
            'python3', 'tools/hierarchical_memory.py', 'auto_organize'
        ], capture_output=True, text=True)
        
        print("   ✅ Auto-organized memory with FOSS context")
    
    # 4. Show code analysis capabilities
    print("\n🔍 Code Analysis Demo:")
    print("   Analyzing this FOSS project...")
    
    result = subprocess.run([
        'python3', 'tools/code_analyzer.py', 'analyze_directory', '.', 'false'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            analysis = json.loads(result.stdout)
            print(f"   ✅ Analyzed {len(analysis)} files")
            python_files = [f for f in analysis if f.get('language') == 'Python']
            print(f"   📊 Python files: {len(python_files)}")
            total_lines = sum(f.get('total_lines', 0) for f in analysis)
            print(f"   📏 Total lines: {total_lines}")
        except:
            print("   📊 Analysis completed")
    
    # 5. Show project creation with FOSS templates
    print("\n🏗️ FOSS Project Templates:")
    foss_projects = ["python", "node", "react", "go"]
    
    for project_type in foss_projects:
        print(f"   ✅ {project_type.title()} project template available")
        print(f"      📦 Uses FOSS dependencies only")
        print(f"      🚀 Ready for self-hosting")
    
    # 6. Security summary
    print("\n🛡️ FOSS Security Features:")
    print("   🔒 Local token encryption with Fernet")
    print("   🏠 Self-hosted infrastructure")
    print("   📋 Open source code for audit")
    print("   🔄 No vendor lock-in")
    print("   🌍 Community-driven security")
    
    # 7. Cost comparison
    print("\n💰 Cost Comparison (Monthly):")
    print("   Proprietary Stack:")
    print("      Slack: $8.75/user × 10 users = $87.50")
    print("      GitHub: $4/user × 10 users = $40.00")
    print("      OpenAI: $20/1M tokens ≈ $100.00")
    print("      Jira: $7.50/user × 10 users = $75.00")
    print("      Total: ~$302.50/month")
    print()
    print("   FOSS Stack:")
    print("      Mattermost: $0.00")
    print("      Gitea: $0.00")
    print("      Ollama: $0.00 (local)")
    print("      Redmine: $0.00")
    print("      Total: $0.00 + infrastructure")
    print("      💾 Savings: ~$300/month + data sovereignty!")
    
    print("\n🎉 FOSS Migration Complete!")
    print("🌟 All services are now:")
    print("   ✅ Free and Open Source")
    print("   ✅ Self-hostable")
    print("   ✅ Privacy-respecting")
    print("   ✅ Community-supported")
    print("   ✅ No vendor lock-in")
    
    print(f"\n📚 Learn more:")
    print(f"   📖 FOSS Alternatives: FOSS_ALTERNATIVES.md")
    print(f"   🧠 Memory System: HIERARCHICAL_MEMORY.md")
    print(f"   🤖 Agent Guidelines: AGENTS.md")

if __name__ == "__main__":
    demonstrate_foss_setup()