#!/usr/bin/env python3

import json
import os
import subprocess
import tempfile
from typing import Dict, List, Any, Optional

class ProjectManager:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def create_project_template(self, project_type: str, project_name: str, base_path: str = ".") -> Dict[str, Any]:
        """Create a new project from template"""
        project_path = os.path.join(base_path, project_name)
        
        try:
            os.makedirs(project_path, exist_ok=True)
            
            if project_type == "python":
                self._create_python_project(project_path, project_name)
            elif project_type == "node":
                self._create_node_project(project_path, project_name)
            elif project_type == "react":
                self._create_react_project(project_path, project_name)
            elif project_type == "go":
                self._create_go_project(project_path, project_name)
            else:
                return {"error": f"Unsupported project type: {project_type}"}
            
            return {
                "success": True,
                "project_path": project_path,
                "project_type": project_type,
                "project_name": project_name
            }
        except Exception as e:
            return {"error": f"Error creating project: {str(e)}"}
    
    def _create_python_project(self, path: str, name: str):
        """Create Python project structure"""
        os.makedirs(os.path.join(path, "src"))
        os.makedirs(os.path.join(path, "tests"))
        
        # Create main.py
        with open(os.path.join(path, "src", "main.py"), 'w') as f:
            f.write(f'#!/usr/bin/env python3\n\n"""\n{name} - Main module\n"""\n\ndef main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()\n')
        
        # Create requirements.txt
        with open(os.path.join(path, "requirements.txt"), 'w') as f:
            f.write("# Add your dependencies here\n")
        
        # Create setup.py
        with open(os.path.join(path, "setup.py"), 'w') as f:
            f.write(f'from setuptools import setup, find_packages\n\nsetup(\n    name="{name}",\n    version="0.1.0",\n    packages=find_packages(),\n    install_requires=[],\n)\n')
        
        # Create test file
        with open(os.path.join(path, "tests", "test_main.py"), 'w') as f:
            f.write(f'import unittest\nfrom src.main import main\n\nclass TestMain(unittest.TestCase):\n    def test_main(self):\n        # Add your tests here\n        pass\n\nif __name__ == "__main__":\n    unittest.main()\n')
    
    def _create_node_project(self, path: str, name: str):
        """Create Node.js project structure"""
        os.makedirs(os.path.join(path, "src"))
        os.makedirs(os.path.join(path, "tests"))
        
        # Create package.json
        package_json = {
            "name": name,
            "version": "1.0.0",
            "description": f"{name} project",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "test": "jest",
                "dev": "nodemon src/index.js"
            },
            "keywords": [],
            "author": "",
            "license": "ISC",
            "dependencies": {},
            "devDependencies": {
                "jest": "^29.0.0",
                "nodemon": "^3.0.0"
            }
        }
        
        with open(os.path.join(path, "package.json"), 'w') as f:
            json.dump(package_json, f, indent=2)
        
        # Create index.js
        with open(os.path.join(path, "src", "index.js"), 'w') as f:
            f.write(f'console.log("Hello, {name}!");\n')
        
        # Create test file
        with open(os.path.join(path, "tests", "index.test.js"), 'w') as f:
            f.write(f'test("{name} basic test", () => {{\n  expect(true).toBe(true);\n}});\n')
    
    def _create_react_project(self, path: str, name: str):
        """Create React project structure"""
        os.makedirs(os.path.join(path, "src"))
        os.makedirs(os.path.join(path, "public"))
        
        # Create package.json
        package_json = {
            "name": name,
            "version": "0.1.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "eslintConfig": {
                "extends": [
                    "react-app",
                    "react-app/jest"
                ]
            },
            "browserslist": {
                "production": [
                    ">0.2%",
                    "not dead",
                    "not op_mini all"
                ],
                "development": [
                    "last 1 chrome version",
                    "last 1 firefox version",
                    "last 1 safari version"
                ]
            }
        }
        
        with open(os.path.join(path, "package.json"), 'w') as f:
            json.dump(package_json, f, indent=2)
        
        # Create public/index.html
        with open(os.path.join(path, "public", "index.html"), 'w') as f:
            f.write(f'<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="utf-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <title>{name}</title>\n</head>\n<body>\n    <div id="root"></div>\n</body>\n</html>\n')
        
        # Create src/App.js
        with open(os.path.join(path, "src", "App.js"), 'w') as f:
            f.write(f'import React from "react";\nimport "./App.css";\n\nfunction App() {{\n  return (\n    <div className="App">\n      <header className="App-header">\n        <h1>Welcome to {name}</h1>\n      </header>\n    </div>\n  );\n}}\n\nexport default App;\n')
        
        # Create src/index.js
        with open(os.path.join(path, "src", "index.js"), 'w') as f:
            f.write(f'import React from "react";\nimport ReactDOM from "react-dom/client";\nimport "./index.css";\nimport App from "./App";\n\nconst root = ReactDOM.createRoot(document.getElementById("root"));\nroot.render(\n  <React.StrictMode>\n    <App />\n  </React.StrictMode>\n);\n')
    
    def _create_go_project(self, path: str, name: str):
        """Create Go project structure"""
        os.makedirs(os.path.join(path, "cmd", name))
        os.makedirs(os.path.join(path, "internal"))
        os.makedirs(os.path.join(path, "pkg"))
        
        # Create go.mod
        result = subprocess.run(['go', 'mod', 'init', name], cwd=path, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Warning: Could not initialize go module: {result.stderr}")
        
        # Create main.go
        with open(os.path.join(path, "cmd", name, "main.go"), 'w') as f:
            f.write(f'package main\n\nimport "fmt"\n\nfunc main() {{\n    fmt.Println("Hello, {name}!")\n}}\n')
    
    def list_projects(self, base_path: str = ".") -> List[Dict[str, Any]]:
        """List all projects in the given directory"""
        projects = []
        
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                project_info = self._detect_project_type(item_path)
                if project_info:
                    project_info["name"] = item
                    project_info["path"] = item_path
                    projects.append(project_info)
        
        return projects
    
    def _detect_project_type(self, path: str) -> Optional[Dict[str, Any]]:
        """Detect project type based on files present"""
        if os.path.exists(os.path.join(path, "package.json")):
            with open(os.path.join(path, "package.json"), 'r') as f:
                package_data = json.load(f)
                dependencies = package_data.get("dependencies", {})
                if "react" in dependencies:
                    return {"type": "react", "framework": "React"}
                else:
                    return {"type": "node", "framework": "Node.js"}
        
        elif os.path.exists(os.path.join(path, "setup.py")) or os.path.exists(os.path.join(path, "pyproject.toml")):
            return {"type": "python", "framework": "Python"}
        
        elif os.path.exists(os.path.join(path, "go.mod")):
            return {"type": "go", "framework": "Go"}
        
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python project_manager.py <action> [args...]")
        print("Actions: create_project, list_projects")
        sys.exit(1)
    
    action = sys.argv[1]
    manager = ProjectManager()
    
    if action == "create_project":
        if len(sys.argv) < 4:
            print("Usage: python project_manager.py create_project <type> <name> [base_path]")
            sys.exit(1)
        
        project_type = sys.argv[2]
        project_name = sys.argv[3]
        base_path = sys.argv[4] if len(sys.argv) > 4 else "."
        
        result = manager.create_project_template(project_type, project_name, base_path)
        print(json.dumps(result, indent=2))
    
    elif action == "list_projects":
        base_path = sys.argv[2] if len(sys.argv) > 2 else "."
        projects = manager.list_projects(base_path)
        print(json.dumps(projects, indent=2))
    
    else:
        print(f"Unknown action: {action}")