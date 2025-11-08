#!/usr/bin/env python3

import json
import os
import subprocess
import hashlib
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
import base64

class FOSSTokenManager:
    def __init__(self, config_path: str = "~/.config/foss_tokens.json"):
        self.config_path = os.path.expanduser(config_path)
        self.config_dir = os.path.dirname(self.config_path)
        self.ensure_config_dir()
        self.encryption_key = self.get_or_create_encryption_key()
        self.tokens = self.load_tokens()
    
    def ensure_config_dir(self):
        """Ensure config directory exists"""
        os.makedirs(self.config_dir, mode=0o700, exist_ok=True)
    
    def get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = os.path.join(self.config_dir, ".key")
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            os.chmod(key_file, 0o600)
            return key
    
    def load_tokens(self) -> Dict[str, Any]:
        """Load encrypted tokens from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'rb') as f:
                    encrypted_data = f.read()
                
                fernet = Fernet(self.encryption_key)
                decrypted_data = fernet.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
            except Exception as e:
                print(f"Error loading tokens: {e}")
                return {}
        return {}
    
    def save_tokens(self):
        """Save encrypted tokens to file"""
        try:
            fernet = Fernet(self.encryption_key)
            data_json = json.dumps(self.tokens, indent=2)
            encrypted_data = fernet.encrypt(data_json.encode())
            
            with open(self.config_path, 'wb') as f:
                f.write(encrypted_data)
            os.chmod(self.config_path, 0o600)
        except Exception as e:
            print(f"Error saving tokens: {e}")
    
    def store_token(self, service: str, token: str, token_type: str = "api_key", 
                   metadata: Optional[Dict] = None):
        """Store a token for a service"""
        self.tokens[service] = {
            "token": token,
            "type": token_type,
            "metadata": metadata or {},
            "created_at": str(subprocess.check_output(['date'], text=True).strip()),
            "last_used": None
        }
        self.save_tokens()
        print(f"Token stored for {service}")
    
    def get_token(self, service: str) -> Optional[str]:
        """Get token for a service"""
        if service in self.tokens:
            # Update last used
            self.tokens[service]["last_used"] = str(subprocess.check_output(['date'], text=True).strip())
            self.save_tokens()
            return self.tokens[service]["token"]
        return None
    
    def get_token_info(self, service: str) -> Optional[Dict]:
        """Get full token information"""
        return self.tokens.get(service)
    
    def list_services(self) -> list:
        """List all stored services"""
        return list(self.tokens.keys())
    
    def delete_token(self, service: str):
        """Delete token for a service"""
        if service in self.tokens:
            del self.tokens[service]
            self.save_tokens()
            print(f"Token deleted for {service}")
        else:
            print(f"No token found for {service}")
    
    def rotate_token(self, service: str, new_token: str):
        """Rotate token for a service"""
        if service in self.tokens:
            old_token = self.tokens[service]["token"]
            self.tokens[service]["token"] = new_token
            self.tokens[service]["rotated_at"] = str(subprocess.check_output(['date'], text=True).strip())
            self.tokens[service]["previous_token_hash"] = hashlib.sha256(old_token.encode()).hexdigest()
            self.save_tokens()
            print(f"Token rotated for {service}")
        else:
            print(f"No token found for {service}")
    
    def export_tokens(self, export_path: str, include_tokens: bool = False):
        """Export token metadata (optionally including actual tokens)"""
        export_data = {}
        
        for service, data in self.tokens.items():
            export_data[service] = {
                "type": data["type"],
                "metadata": data["metadata"],
                "created_at": data["created_at"],
                "last_used": data["last_used"]
            }
            
            if include_tokens:
                export_data[service]["token"] = data["token"]
            else:
                # Only include token hash for security
                export_data[service]["token_hash"] = hashlib.sha256(data["token"].encode()).hexdigest()
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Token metadata exported to {export_path}")
    
    def import_tokens(self, import_path: str):
        """Import tokens from file"""
        try:
            with open(import_path, 'r') as f:
                import_data = json.load(f)
            
            for service, data in import_data.items():
                if "token" in data:
                    self.store_token(service, data["token"], data.get("type", "api_key"), data.get("metadata", {}))
                else:
                    print(f"Skipping {service} - no token found")
            
            print("Token import completed")
        except Exception as e:
            print(f"Error importing tokens: {e}")
    
    def generate_service_token(self, service: str, length: int = 32) -> str:
        """Generate a random token for a service"""
        import secrets
        token = base64.urlsafe_b64encode(secrets.token_bytes(length)).decode()
        self.store_token(service, token, "generated", {"length": length, "auto_generated": True})
        return token
    
    def check_token_expiry(self, service: str, max_days: int = 90) -> bool:
        """Check if token is older than max_days"""
        if service not in self.tokens:
            return False
        
        created_at = self.tokens[service].get("created_at")
        if not created_at:
            return True
        
        # Simple date check (in production, use proper date parsing)
        return "days ago" in subprocess.check_output([
            'echo', f"$(($(date +%s) - $(date -d '{created_at}' +%s))) / 86400"
        ], shell=True, text=True).strip() and int(subprocess.check_output([
            'echo', f"$(($(date +%s) - $(date -d '{created_at}' +%s))) / 86400"
        ], shell=True, text=True).strip()) > max_days
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get security summary of stored tokens"""
        summary = {
            "total_tokens": len(self.tokens),
            "services": list(self.tokens.keys()),
            "token_types": {},
            "old_tokens": [],
            "recently_used": []
        }
        
        for service, data in self.tokens.items():
            # Count token types
            token_type = data.get("type") if data else "unknown"
            summary["token_types"][token_type] = summary["token_types"].get(token_type, 0) + 1
            
            # Check for old tokens (simplified)
            try:
                if self.check_token_expiry(service, 90):
                    summary["old_tokens"].append(service)
            except:
                pass
            
            # Check recently used tokens
            try:
                last_used = data.get("last_used") if data else None
                if last_used and "days ago" not in str(last_used):
                    summary["recently_used"].append(service)
            except:
                pass
        
        return summary

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python foss_token_manager.py <action> [args...]")
        print("Actions: store, get, list, delete, rotate, export, import, generate, summary")
        sys.exit(1)
    
    action = sys.argv[1]
    manager = FOSSTokenManager()
    
    if action == "store":
        if len(sys.argv) < 4:
            print("Usage: python foss_token_manager.py store <service> <token> [type]")
            sys.exit(1)
        service = sys.argv[2]
        token = sys.argv[3]
        token_type = sys.argv[4] if len(sys.argv) > 4 else "api_key"
        manager.store_token(service, token, token_type)
    
    elif action == "get":
        if len(sys.argv) < 3:
            print("Usage: python foss_token_manager.py get <service>")
            sys.exit(1)
        service = sys.argv[2]
        token = manager.get_token(service)
        if token:
            print(token)
        else:
            print(f"No token found for {service}")
    
    elif action == "list":
        services = manager.list_services()
        print("Stored services:")
        for service in services:
            info = manager.get_token_info(service)
            if info:
                last_used = info.get("last_used", "Never")
                token_type = info.get('type', 'unknown')
            else:
                last_used = "Never"
                token_type = "unknown"
            print(f"  - {service} ({token_type}) - Last used: {last_used}")
    
    elif action == "delete":
        if len(sys.argv) < 3:
            print("Usage: python foss_token_manager.py delete <service>")
            sys.exit(1)
        service = sys.argv[2]
        manager.delete_token(service)
    
    elif action == "rotate":
        if len(sys.argv) < 4:
            print("Usage: python foss_token_manager.py rotate <service> <new_token>")
            sys.exit(1)
        service = sys.argv[2]
        new_token = sys.argv[3]
        manager.rotate_token(service, new_token)
    
    elif action == "export":
        if len(sys.argv) < 3:
            print("Usage: python foss_token_manager.py export <file_path> [--include-tokens]")
            sys.exit(1)
        export_path = sys.argv[2]
        include_tokens = "--include-tokens" in sys.argv
        manager.export_tokens(export_path, include_tokens)
    
    elif action == "import":
        if len(sys.argv) < 3:
            print("Usage: python foss_token_manager.py import <file_path>")
            sys.exit(1)
        import_path = sys.argv[2]
        manager.import_tokens(import_path)
    
    elif action == "generate":
        if len(sys.argv) < 3:
            print("Usage: python foss_token_manager.py generate <service> [length]")
            sys.exit(1)
        service = sys.argv[2]
        length = int(sys.argv[3]) if len(sys.argv) > 3 else 32
        token = manager.generate_service_token(service, length)
        print(f"Generated token for {service}: {token}")
    
    elif action == "summary":
        summary = manager.get_security_summary()
        print(json.dumps(summary, indent=2))
    
    else:
        print(f"Unknown action: {action}")