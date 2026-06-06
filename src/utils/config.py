"""
配置管理模組
"""

import json
import os
from pathlib import Path

class ConfigManager:
    """配置檔案管理器"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = {}
        self.load()
    
    def load(self):
        """載入配置檔案"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"⚠️ 載入配置檔案失敗: {e}，使用預設配置")
                self.config = self._default_config()
        else:
            self.config = self._default_config()
            self.save()
    
    def save(self):
        """保存配置檔案"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 保存配置檔案失敗: {e}")
    
    def get(self, key, default=None):
        """獲取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """設定配置值"""
        self.config[key] = value
        self.save()
    
    def update(self, data):
        """更新多個配置值"""
        self.config.update(data)
        self.save()
    
    @staticmethod
    def _default_config():
        """預設配置"""
        return {
            "source_language": "en",
            "target_language": "zh-TW",
            "float_window_enabled": True,
            "clipboard_monitor_enabled": True,
            "ocr_enabled": True,
            "auto_copy_result": True,
            "theme": "dark",
            "font_size": 12,
            "api_timeout": 10,
            "notification_enabled": True
        }


# 全域配置實例
config_manager = ConfigManager()
