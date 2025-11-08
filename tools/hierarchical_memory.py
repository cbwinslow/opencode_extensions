#!/usr/bin/env python3

import json
import sqlite3
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

class HierarchicalMemoryManager:
    def __init__(self, db_path: str = "hierarchical_memory.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize hierarchical SQLite database for memory storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Hierarchical memory nodes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_nodes (
                id TEXT PRIMARY KEY,
                parent_id TEXT,
                node_type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                metadata TEXT,
                weight REAL DEFAULT 1.0,
                access_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES memory_nodes(id) ON DELETE CASCADE
            )
        ''')
        
        # Node relationships for complex hierarchies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS node_relationships (
                id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL DEFAULT 1.0,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES memory_nodes(id) ON DELETE CASCADE,
                FOREIGN KEY (target_id) REFERENCES memory_nodes(id) ON DELETE CASCADE
            )
        ''')
        
        # Tags for categorization
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#007acc',
                description TEXT
            )
        ''')
        
        # Node-tag relationships
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS node_tags (
                node_id TEXT NOT NULL,
                tag_id TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                PRIMARY KEY (node_id, tag_id),
                FOREIGN KEY (node_id) REFERENCES memory_nodes(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        ''')
        
        # Sessions for conversation tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                root_node_id TEXT,
                title TEXT,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (root_node_id) REFERENCES memory_nodes(id) ON DELETE SET NULL
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_nodes_parent ON memory_nodes(parent_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_nodes_type ON memory_nodes(node_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_nodes_weight ON memory_nodes(weight)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relationships_source ON node_relationships(source_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relationships_target ON node_relationships(target_id)')
        
        conn.commit()
        conn.close()
    
    def create_node(self, node_type: str, title: str, content: str = "", 
                   parent_id: Optional[str] = None, metadata: Optional[Dict] = None,
                   weight: float = 1.0) -> str:
        """Create a new memory node"""
        node_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memory_nodes (id, parent_id, node_type, title, content, metadata, weight)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (node_id, parent_id, node_type, title, content, json.dumps(metadata or {}), weight))
        
        conn.commit()
        conn.close()
        return node_id
    
    def create_session(self, title: str, metadata: Optional[Dict] = None) -> str:
        """Create a new session with root node"""
        session_id = str(uuid.uuid4())
        root_node_id = self.create_node("session_root", f"Session: {title}", 
                                       metadata=metadata, weight=2.0)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (id, root_node_id, title, metadata)
            VALUES (?, ?, ?, ?)
        ''', (session_id, root_node_id, title, json.dumps(metadata or {})))
        
        conn.commit()
        conn.close()
        return session_id
    
    def add_conversation_turn(self, session_id: str, role: str, content: str, 
                           metadata: Optional[Dict] = None) -> str:
        """Add conversation turn to session"""
        # Get session root node
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT root_node_id FROM sessions WHERE id = ?', (session_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise ValueError(f"Session {session_id} not found")
        
        root_node_id = result[0]
        
        # Create conversation node
        conv_metadata = {
            "role": role,
            "session_id": session_id,
            **(metadata or {})
        }
        
        return self.create_node("conversation", f"{role.title()}: {content[:50]}...", 
                              content, root_node_id, conv_metadata)
    
    def create_concept_node(self, concept: str, definition: str, 
                          parent_concepts: Optional[List[str]] = None,
                          tags: Optional[List[str]] = None) -> str:
        """Create a concept node with hierarchical relationships"""
        # Find or create parent concept node
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM memory_nodes WHERE node_type = "concepts_root"')
        result = cursor.fetchone()
        
        if result:
            concepts_root_id = result[0]
        else:
            concepts_root_id = self.create_node("concepts_root", "Concepts Root", 
                                             weight=3.0)
        
        conn.close()
        
        # Create concept node
        metadata = {"definition": definition, "type": "concept"}
        node_id = self.create_node("concept", concept, definition, concepts_root_id, metadata)
        
        # Create relationships to parent concepts
        if parent_concepts:
            for parent in parent_concepts:
                self.create_relationship(node_id, parent, "is_a", 0.8)
        
        # Add tags
        if tags:
            for tag in tags:
                self.add_tag_to_node(node_id, tag)
        
        return node_id
    
    def create_relationship(self, source_id: str, target_id: str, 
                          relationship_type: str, strength: float = 1.0,
                          metadata: Optional[Dict] = None):
        """Create relationship between nodes"""
        relationship_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO node_relationships (id, source_id, target_id, relationship_type, strength, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (relationship_id, source_id, target_id, relationship_type, strength, json.dumps(metadata or {})))
        
        conn.commit()
        conn.close()
    
    def get_node_hierarchy(self, node_id: str, max_depth: int = 5) -> Dict[str, Any]:
        """Get hierarchical tree starting from node"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        def build_tree(current_id: str, depth: int = 0) -> Dict[str, Any]:
            if depth >= max_depth:
                return {}
            
            cursor.execute('''
                SELECT id, node_type, title, content, metadata, weight, access_count
                FROM memory_nodes WHERE id = ?
            ''', (current_id,))
            
            node_data = cursor.fetchone()
            if not node_data:
                return {}
            
            node_dict = {
                "id": node_data[0],
                "type": node_data[1],
                "title": node_data[2],
                "content": node_data[3],
                "metadata": json.loads(node_data[4]),
                "weight": node_data[5],
                "access_count": node_data[6],
                "children": []
            }
            
            # Get children
            cursor.execute('''
                SELECT id FROM memory_nodes WHERE parent_id = ? ORDER BY weight DESC, created_at ASC
            ''', (current_id,))
            
            children = cursor.fetchall()
            for child in children:
                child_tree = build_tree(child[0], depth + 1)
                if child_tree:
                    node_dict["children"].append(child_tree)
            
            return node_dict
        
        hierarchy = build_tree(node_id)
        conn.close()
        return hierarchy
    
    def find_related_nodes(self, node_id: str, relationship_types: Optional[List[str]] = None,
                          max_distance: int = 2) -> List[Dict[str, Any]]:
        """Find nodes related through relationships"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if relationship_types:
            placeholders = ','.join(['?' for _ in relationship_types])
            cursor.execute(f'''
                SELECT DISTINCT target_id, relationship_type, strength
                FROM node_relationships 
                WHERE source_id = ? AND relationship_type IN ({placeholders})
                UNION
                SELECT DISTINCT source_id, relationship_type, strength
                FROM node_relationships 
                WHERE target_id = ? AND relationship_type IN ({placeholders})
            ''', [node_id] + relationship_types + [node_id] + relationship_types)
        else:
            cursor.execute('''
                SELECT DISTINCT target_id, relationship_type, strength
                FROM node_relationships WHERE source_id = ?
                UNION
                SELECT DISTINCT source_id, relationship_type, strength
                FROM node_relationships WHERE target_id = ?
            ''', (node_id, node_id))
        
        related_nodes = []
        for row in cursor.fetchall():
            related_nodes.append({
                "node_id": row[0],
                "relationship_type": row[1],
                "strength": row[2]
            })
        
        conn.close()
        return related_nodes
    
    def create_tag(self, name: str, color: str = "#007acc", 
                  description: str = "") -> str:
        """Create a new tag"""
        tag_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO tags (id, name, color, description)
            VALUES (?, ?, ?, ?)
        ''', (tag_id, name, color, description))
        
        conn.commit()
        conn.close()
        return tag_id
    
    def add_tag_to_node(self, node_id: str, tag_name: str, confidence: float = 1.0):
        """Add tag to node"""
        # Get or create tag
        tag_id = self.create_tag(tag_name)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO node_tags (node_id, tag_id, confidence)
            VALUES (?, ?, ?)
        ''', (node_id, tag_id, confidence))
        
        conn.commit()
        conn.close()
    
    def search_by_tag(self, tag_name: str) -> List[Dict[str, Any]]:
        """Find nodes by tag"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT n.id, n.node_type, n.title, n.content, n.metadata, nt.confidence
            FROM memory_nodes n
            JOIN node_tags nt ON n.id = nt.node_id
            JOIN tags t ON nt.tag_id = t.id
            WHERE t.name = ?
            ORDER BY nt.confidence DESC, n.weight DESC
        ''', (tag_name,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "type": row[1],
                "title": row[2],
                "content": row[3],
                "metadata": json.loads(row[4]),
                "tag_confidence": row[5]
            })
        
        conn.close()
        return results
    
    def get_memory_graph(self, center_node_id: Optional[str] = None, radius: int = 2) -> Dict[str, Any]:
        """Get memory as a graph structure"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if center_node_id:
            # Get subgraph around center node
            cursor.execute('''
                SELECT id, node_type, title, weight FROM memory_nodes
                WHERE id = ? OR parent_id IN (
                    SELECT id FROM memory_nodes WHERE parent_id = ?
                )
            ''', (center_node_id, center_node_id))
        else:
            # Get all nodes
            cursor.execute('SELECT id, node_type, title, weight FROM memory_nodes LIMIT 100')
        
        nodes = []
        for row in cursor.fetchall():
            nodes.append({
                "id": row[0],
                "type": row[1],
                "title": row[2],
                "weight": row[3]
            })
        
        # Get relationships
        cursor.execute('''
            SELECT source_id, target_id, relationship_type, strength
            FROM node_relationships
            WHERE source_id IN (SELECT id FROM memory_nodes LIMIT 100)
            AND target_id IN (SELECT id FROM memory_nodes LIMIT 100)
        ''')
        
        relationships = []
        for row in cursor.fetchall():
            relationships.append({
                "source": row[0],
                "target": row[1],
                "type": row[2],
                "strength": row[3]
            })
        
        conn.close()
        
        return {
            "nodes": nodes,
            "relationships": relationships
        }
    
    def auto_organize_memory(self):
        """Automatically organize memory based on content and relationships"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find unorganized conversation nodes
        cursor.execute('''
            SELECT id, content FROM memory_nodes 
            WHERE node_type = "conversation" AND parent_id NOT IN (
                SELECT id FROM memory_nodes WHERE node_type = "session_root"
            )
        ''')
        
        unorganized = cursor.fetchall()
        
        for node_id, content in unorganized:
            # Simple content analysis for organization
            content_lower = content.lower()
            
            # Categorize based on keywords
            if any(keyword in content_lower for keyword in ['error', 'bug', 'fix']):
                self.add_tag_to_node(node_id, "debugging")
            elif any(keyword in content_lower for keyword in ['test', 'spec', 'assert']):
                self.add_tag_to_node(node_id, "testing")
            elif any(keyword in content_lower for keyword in ['deploy', 'production', 'release']):
                self.add_tag_to_node(node_id, "deployment")
            elif any(keyword in content_lower for keyword in ['api', 'endpoint', 'request']):
                self.add_tag_to_node(node_id, "api")
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python hierarchical_memory.py <action> [args...]")
        print("Actions: create_session, add_conversation, create_concept, get_hierarchy, search_tag, auto_organize")
        sys.exit(1)
    
    action = sys.argv[1]
    memory = HierarchicalMemoryManager()
    
    if action == "create_session":
        title = sys.argv[2] if len(sys.argv) > 2 else "New Session"
        session_id = memory.create_session(title)
        print(f"Created session: {session_id}")
    
    elif action == "add_conversation":
        session_id = sys.argv[2]
        role = sys.argv[3]
        content = sys.argv[4]
        node_id = memory.add_conversation_turn(session_id, role, content)
        print(f"Added conversation node: {node_id}")
    
    elif action == "create_concept":
        concept = sys.argv[2]
        definition = sys.argv[3]
        parents = sys.argv[4].split(',') if len(sys.argv) > 4 else []
        tags = sys.argv[5].split(',') if len(sys.argv) > 5 else []
        node_id = memory.create_concept_node(concept, definition, parents, tags)
        print(f"Created concept node: {node_id}")
    
    elif action == "get_hierarchy":
        node_id = sys.argv[2]
        hierarchy = memory.get_node_hierarchy(node_id)
        print(json.dumps(hierarchy, indent=2))
    
    elif action == "search_tag":
        tag_name = sys.argv[2]
        nodes = memory.search_by_tag(tag_name)
        print(json.dumps(nodes, indent=2))
    
    elif action == "auto_organize":
        memory.auto_organize_memory()
        print("Memory auto-organization completed")
    
    else:
        print(f"Unknown action: {action}")