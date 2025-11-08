#!/usr/bin/env python3

import json
import os
import subprocess
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime

class CodeAnalyzer:
    def __init__(self):
        self.supported_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rs'}
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file for code metrics"""
        if not os.path.exists(file_path):
            return {"error": f"File {file_path} does not exist"}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            total_lines = len(lines)
            non_empty_lines = len([line for line in lines if line.strip()])
            comment_lines = self._count_comments(content, file_path)
            
            with open(file_path, 'rb') as f:
                content_hash = hashlib.md5(f.read()).hexdigest()
            
            return {
                "file_path": file_path,
                "total_lines": total_lines,
                "non_empty_lines": non_empty_lines,
                "comment_lines": comment_lines,
                "content_hash": content_hash,
                "file_size": os.path.getsize(file_path),
                "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                "language": self._detect_language(file_path)
            }
        except Exception as e:
            return {"error": f"Error analyzing {file_path}: {str(e)}"}
    
    def analyze_directory(self, directory: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """Analyze all supported files in a directory"""
        results = []
        
        if recursive:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if any(file.endswith(ext) for ext in self.supported_extensions):
                        file_path = os.path.join(root, file)
                        results.append(self.analyze_file(file_path))
        else:
            for file in os.listdir(directory):
                if any(file.endswith(ext) for ext in self.supported_extensions):
                    file_path = os.path.join(directory, file)
                    results.append(self.analyze_file(file_path))
        
        return results
    
    def _count_comments(self, content: str, file_path: str) -> int:
        """Count comment lines based on file type"""
        ext = os.path.splitext(file_path)[1]
        
        if ext in {'.py'}:
            lines = content.split('\n')
            return sum(1 for line in lines if line.strip().startswith('#'))
        elif ext in {'.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.cs', '.go'}:
            lines = content.split('\n')
            return sum(1 for line in lines if line.strip().startswith('//') or line.strip().startswith('/*'))
        else:
            return 0
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language based on file extension"""
        ext = os.path.splitext(file_path)[1]
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Header',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust'
        }
        return language_map.get(ext, 'Unknown')
    
    def find_duplicates(self, directory: str) -> List[Dict[str, Any]]:
        """Find duplicate files based on content hash"""
        file_hashes = {}
        duplicates = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.supported_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            content_hash = hashlib.md5(f.read()).hexdigest()
                        
                        if content_hash in file_hashes:
                            duplicates.append({
                                "hash": content_hash,
                                "files": [file_hashes[content_hash], file_path]
                            })
                        else:
                            file_hashes[content_hash] = file_path
                    except Exception:
                        continue
        
        return duplicates

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python code_analyzer.py <action> <path> [recursive]")
        print("Actions: analyze_file, analyze_directory, find_duplicates")
        sys.exit(1)
    
    action = sys.argv[1]
    path = sys.argv[2]
    recursive = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else True
    
    analyzer = CodeAnalyzer()
    
    if action == "analyze_file":
        result = analyzer.analyze_file(path)
        print(json.dumps(result, indent=2))
    
    elif action == "analyze_directory":
        results = analyzer.analyze_directory(path, recursive)
        print(json.dumps(results, indent=2))
    
    elif action == "find_duplicates":
        duplicates = analyzer.find_duplicates(path)
        print(json.dumps(duplicates, indent=2))
    
    else:
        print(f"Unknown action: {action}")