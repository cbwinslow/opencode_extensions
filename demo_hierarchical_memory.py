#!/usr/bin/env python3

import json
import subprocess
import sys

def run_hierarchical_memory_demo():
    """Run demonstration of hierarchical memory system"""
    print("🧠 Hierarchical Memory System Demo")
    print("=" * 50)
    
    # Initialize the hierarchical memory manager
    print("\n1. Creating a new session...")
    result = subprocess.run([
        'python3', 'tools/hierarchical_memory.py', 'create_session', 
        'OpenAI Integration Session'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        session_id = result.stdout.strip().split(': ')[1]
        print(f"   Session ID: {session_id}")
    else:
        print(f"   Error: {result.stderr}")
        return
    
    # Add conversation turns
    print("\n2. Adding conversation turns...")
    conversations = [
        ("user", "How do I integrate OpenAI API with my Python application?"),
        ("assistant", "You can use the openai Python package. First install it with pip install openai, then set up your API key."),
        ("user", "What about error handling for API calls?")
    ]
    
    for role, content in conversations:
        result = subprocess.run([
            'python3', 'tools/hierarchical_memory.py', 'add_conversation',
            session_id, role, content
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"   Error adding conversation: {result.stderr}")
    
    print(f"   Added {len(conversations)} conversation turns")
    
    # Create concept nodes
    print("\n3. Creating concept nodes...")
    concepts = [
        ("API Integration", "The process of connecting different software systems through defined interfaces", "", "programming,integration"),
        ("Python", "A high-level programming language known for its simplicity and readability", "", "language,programming"),
        ("OpenAI", "An AI research company that provides powerful language models via API", "API Integration", "ai,machine-learning")
    ]
    
    for concept, definition, parents, tags in concepts:
        result = subprocess.run([
            'python3', 'tools/hierarchical_memory.py', 'create_concept',
            concept, definition, parents, tags
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"   Error creating concept: {result.stderr}")
    
    print(f"   Created {len(concepts)} concept nodes")
    
    # Auto-organize memory
    print("\n4. Auto-organizing memory...")
    result = subprocess.run([
        'python3', 'tools/hierarchical_memory.py', 'auto_organize'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("   Memory auto-organization completed")
    else:
        print(f"   Error: {result.stderr}")
    
    # Get session hierarchy
    print("\n5. Session hierarchy:")
    result = subprocess.run([
        'python3', 'tools/hierarchical_memory.py', 'get_hierarchy', session_id
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            hierarchy = json.loads(result.stdout)
            print(json.dumps(hierarchy, indent=6))
        except:
            print(result.stdout)
    else:
        print(f"   Error: {result.stderr}")
    
    # Search by tags
    print("\n6. Searching by tag 'programming':")
    result = subprocess.run([
        'python3', 'tools/hierarchical_memory.py', 'search_tag', 'programming'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            tagged_nodes = json.loads(result.stdout)
            for node in tagged_nodes:
                print(f"   - {node['title']}")
        except:
            print(result.stdout)
    else:
        print(f"   Error: {result.stderr}")
    
    print("\n✅ Demo completed! The memory system has organized information hierarchically.")
    print("\n📊 Summary:")
    print(f"   - Sessions: 1")
    print(f"   - Conversation nodes: 3")
    print(f"   - Concept nodes: 3")
    print(f"   - Tags: Multiple")
    
    print(f"\n💾 Database saved as: hierarchical_memory.db")
    print("\n🔍 You can explore the memory using:")
    print(f"   python cli.py hierarchical_memory get_hierarchy {session_id}")
    print(f"   python cli.py hierarchical_memory search_tag programming")

if __name__ == "__main__":
    run_hierarchical_memory_demo()