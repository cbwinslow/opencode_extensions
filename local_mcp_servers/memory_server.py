#!/usr/bin/env python3
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
