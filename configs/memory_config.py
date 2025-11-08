#!/usr/bin/env python3

import json
import os
from typing import Dict, Any, Optional

class MemoryConfigManager:
    def __init__(self, config_path: str = "memory_config.json"):
        self.config_path = config_path
        self.default_config = {
            "memory_settings": {
                "max_conversation_history": 100,
                "max_context_entries": 50,
                "auto_cleanup_days": 30,
                "compression_threshold": 1000,
                "enable_persistence": True
            },
            "database_settings": {
                "db_path": "memory.db",
                "backup_enabled": True,
                "backup_interval_hours": 24,
                "max_backup_files": 7
            },
            "performance_settings": {
                "cache_size_mb": 100,
                "index_conversations": True,
                "batch_size": 1000,
                "connection_pool_size": 5
            },
            "privacy_settings": {
                "encrypt_sensitive_data": True,
                "anonymize_user_data": False,
                "data_retention_days": 90,
                "auto_delete_expired": True
            },
            "integration_settings": {
                "sync_with_external": False,
                "export_format": "json",
                "import_on_startup": False,
                "sync_interval_minutes": 60
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_configs(self.default_config, loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.default_config.copy()
        else:
            self.save_config(self.default_config)
            return self.default_config.copy()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """Save configuration to file"""
        config_to_save = config or self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            if config:
                self.config = config
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_setting(self, key_path: str, default: Any = None) -> Any:
        """Get a setting using dot notation (e.g., 'memory_settings.max_conversation_history')"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set_setting(self, key_path: str, value: Any):
        """Set a setting using dot notation"""
        keys = key_path.split('.')
        config_section = self.config
        
        for key in keys[:-1]:
            if key not in config_section:
                config_section[key] = {}
            config_section = config_section[key]
        
        config_section[keys[-1]] = value
        self.save_config()
    
    def _merge_configs(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge loaded config with defaults"""
        merged = default.copy()
        
        for key, value in loaded.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.default_config.copy()
        self.save_config()
    
    def export_config(self, export_path: str):
        """Export configuration to file"""
        try:
            with open(export_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, import_path: str):
        """Import configuration from file"""
        try:
            with open(import_path, 'r') as f:
                imported_config = json.load(f)
            self.config = self._merge_configs(self.default_config, imported_config)
            self.save_config()
            return True
        except Exception as e:
            print(f"Error importing config: {e}")
            return False
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate configuration and return issues"""
        issues = []
        
        # Validate memory settings
        max_history = self.get_setting('memory_settings.max_conversation_history')
        if not isinstance(max_history, int) or max_history < 1:
            issues.append("memory_settings.max_conversation_history must be a positive integer")
        
        cleanup_days = self.get_setting('memory_settings.auto_cleanup_days')
        if not isinstance(cleanup_days, int) or cleanup_days < 1:
            issues.append("memory_settings.auto_cleanup_days must be a positive integer")
        
        # Validate database settings
        db_path = self.get_setting('database_settings.db_path')
        if not isinstance(db_path, str) or not db_path.strip():
            issues.append("database_settings.db_path must be a non-empty string")
        
        # Validate performance settings
        cache_size = self.get_setting('performance_settings.cache_size_mb')
        if not isinstance(cache_size, int) or cache_size < 1:
            issues.append("performance_settings.cache_size_mb must be a positive integer")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of current memory configuration"""
        return {
            "max_conversation_history": self.get_setting('memory_settings.max_conversation_history'),
            "auto_cleanup_days": self.get_setting('memory_settings.auto_cleanup_days'),
            "persistence_enabled": self.get_setting('memory_settings.enable_persistence'),
            "encryption_enabled": self.get_setting('privacy_settings.encrypt_sensitive_data'),
            "data_retention_days": self.get_setting('privacy_settings.data_retention_days'),
            "cache_size_mb": self.get_setting('performance_settings.cache_size_mb'),
            "sync_enabled": self.get_setting('integration_settings.sync_with_external')
        }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python memory_config.py <action> [args...]")
        print("Actions: get, set, reset, validate, summary, export, import")
        sys.exit(1)
    
    action = sys.argv[1]
    config_manager = MemoryConfigManager()
    
    if action == "get":
        if len(sys.argv) < 3:
            print("Usage: python memory_config.py get <key_path>")
            sys.exit(1)
        key_path = sys.argv[2]
        value = config_manager.get_setting(key_path)
        print(json.dumps(value, indent=2))
    
    elif action == "set":
        if len(sys.argv) < 4:
            print("Usage: python memory_config.py set <key_path> <value>")
            sys.exit(1)
        key_path = sys.argv[2]
        value_str = sys.argv[3]
        
        # Try to parse as JSON, fallback to string
        try:
            value = json.loads(value_str)
        except:
            value = value_str
        
        config_manager.set_setting(key_path, value)
        print(f"Set {key_path} = {value}")
    
    elif action == "reset":
        config_manager.reset_to_defaults()
        print("Configuration reset to defaults")
    
    elif action == "validate":
        validation = config_manager.validate_config()
        print(json.dumps(validation, indent=2))
    
    elif action == "summary":
        summary = config_manager.get_memory_summary()
        print(json.dumps(summary, indent=2))
    
    elif action == "export":
        if len(sys.argv) < 3:
            print("Usage: python memory_config.py export <file_path>")
            sys.exit(1)
        export_path = sys.argv[2]
        success = config_manager.export_config(export_path)
        print(f"Export {'successful' if success else 'failed'}")
    
    elif action == "import":
        if len(sys.argv) < 3:
            print("Usage: python memory_config.py import <file_path>")
            sys.exit(1)
        import_path = sys.argv[2]
        success = config_manager.import_config(import_path)
        print(f"Import {'successful' if success else 'failed'}")
    
    else:
        print(f"Unknown action: {action}")