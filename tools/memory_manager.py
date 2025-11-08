#!/usr/bin/env python3

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class MemoryManager:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for memory storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(session_id, key)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                UNIQUE(file_path, content_hash)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_conversation(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """Store conversation turn"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (session_id, role, content, metadata)
            VALUES (?, ?, ?, ?)
        ''', (session_id, role, content, json.dumps(metadata or {})))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Retrieve conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role, content, metadata, timestamp
            FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'role': row[0],
                'content': row[1],
                'metadata': json.loads(row[2]),
                'timestamp': row[3]
            })
        
        conn.close()
        return list(reversed(results))
    
    def store_context(self, session_id: str, key: str, value: str):
        """Store context information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO context (session_id, key, value)
            VALUES (?, ?, ?)
        ''', (session_id, key, value))
        
        conn.commit()
        conn.close()
    
    def get_context(self, session_id: str, key: Optional[str] = None) -> Dict[str, str]:
        """Retrieve context information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if key:
            cursor.execute('''
                SELECT value FROM context WHERE session_id = ? AND key = ?
            ''', (session_id, key))
            result = cursor.fetchone()
            conn.close()
            return {key: result[0]} if result else {}
        else:
            cursor.execute('''
                SELECT key, value FROM context WHERE session_id = ?
            ''', (session_id,))
            results = dict(cursor.fetchall())
            conn.close()
            return results
    
    def store_file_memory(self, file_path: str, content_hash: str, metadata: Optional[Dict] = None):
        """Store file information for memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO file_memory (file_path, content_hash, metadata)
            VALUES (?, ?, ?)
        ''', (file_path, content_hash, json.dumps(metadata or {})))
        
        conn.commit()
        conn.close()
    
    def get_file_memory(self, file_path: Optional[str] = None) -> List[Dict]:
        """Retrieve file memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if file_path:
            cursor.execute('''
                SELECT file_path, content_hash, metadata, last_modified
                FROM file_memory
                WHERE file_path = ?
                ORDER BY last_modified DESC
            ''', (file_path,))
        else:
            cursor.execute('''
                SELECT file_path, content_hash, metadata, last_modified
                FROM file_memory
                ORDER BY last_modified DESC
                LIMIT 100
            ''')
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'file_path': row[0],
                'content_hash': row[1],
                'metadata': json.loads(row[2]),
                'last_modified': row[3]
            })
        
        conn.close()
        return results
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old data to prevent database bloat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now().replace(tzinfo=None).timestamp() - (days * 24 * 3600)
        
        cursor.execute('''
            DELETE FROM conversations WHERE timestamp < datetime(?, 'unixepoch')
        ''', (cutoff_date,))
        
        cursor.execute('''
            DELETE FROM file_memory WHERE last_modified < datetime(?, 'unixepoch')
        ''', (cutoff_date,))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    import sys
    import hashlib
    
    if len(sys.argv) < 3:
        print("Usage: python memory_manager.py <action> [args...]")
        print("Actions: store_conversation, get_history, store_context, get_context, store_file, get_file, cleanup")
        sys.exit(1)
    
    action = sys.argv[1]
    memory = MemoryManager()
    
    if action == "store_conversation":
        session_id = sys.argv[2]
        role = sys.argv[3]
        content = sys.argv[4]
        memory.store_conversation(session_id, role, content)
        print("Conversation stored successfully")
    
    elif action == "get_history":
        session_id = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        history = memory.get_conversation_history(session_id, limit)
        print(json.dumps(history, indent=2))
    
    elif action == "store_context":
        session_id = sys.argv[2]
        key = sys.argv[3]
        value = sys.argv[4]
        memory.store_context(session_id, key, value)
        print("Context stored successfully")
    
    elif action == "get_context":
        session_id = sys.argv[2]
        key = sys.argv[3] if len(sys.argv) > 3 else None
        context = memory.get_context(session_id, key) if key else memory.get_context(session_id)
        print(json.dumps(context, indent=2))
    
    elif action == "store_file":
        file_path = sys.argv[2]
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content_hash = hashlib.md5(f.read()).hexdigest()
            memory.store_file_memory(file_path, content_hash)
            print("File memory stored successfully")
        else:
            print(f"File {file_path} does not exist")
    
    elif action == "get_file":
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
        files = memory.get_file_memory(file_path) if file_path else memory.get_file_memory()
        print(json.dumps(files, indent=2))
    
    elif action == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        memory.cleanup_old_data(days)
        print(f"Cleaned up data older than {days} days")
    
    else:
        print(f"Unknown action: {action}")