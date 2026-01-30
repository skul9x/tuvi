import json
import os
from core.constants import STAR_SCORES
from core.encryption import EncryptionManager

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "api_key": "",
    "model": "models/gemini-2.0-flash",
    "star_scores": STAR_SCORES,
    "theme": "LIGHT"
}

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.config = DEFAULT_CONFIG.copy()
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    
                    # Decrypt API Key if it exists
                    if "api_key" in saved_config and saved_config["api_key"]:
                        # Detect if it's already encrypted or legacy plain text?
                        # Fernet tokens are long and start with specific signatures, but simple way:
                        # Try decrypt. If fail, assume plain text (legacy migration).
                        try:
                            decrypted = EncryptionManager.decrypt(saved_config["api_key"])
                            if not decrypted and saved_config["api_key"]: 
                                # Decrypt returned empty but we have data -> Decryption failed. 
                                # Could be legacy plain text.
                                pass 
                            else:
                                saved_config["api_key"] = decrypted
                        except:
                            # Keep as is (Legacy plain text)
                            pass
                            
                    self.config.update(saved_config)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save_config(self):
        try:
            # Create a copy to save (don't modify self.config in memory which needs plain text for usage)
            config_to_save = self.config.copy()
            
            # Encrypt API Key
            if config_to_save["api_key"]:
                config_to_save["api_key"] = EncryptionManager.encrypt(config_to_save["api_key"])
                
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
