"""
剪貼板監控模組
"""

import time
import pyperclip
import threading
from typing import Callable, Optional
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)

class ClipboardMonitor:
    """剪貼板監控器 - 監控剪貼板變化"""
    
    def __init__(self, callback: Optional[Callable] = None, 
                 check_interval: float = 0.5):
        """
        初始化剪貼板監控器
        
        Args:
            callback: 剪貼板內容變化時的回調函數
            check_interval: 檢查間隔（秒）
        """
        self.callback = callback
        self.check_interval = check_interval
        self.is_running = False
        self.monitor_thread = None
        self.last_clipboard = ""
        
        logger.info("📋 剪貼板監控器已初始化")
    
    def start(self):
        """開始監控剪貼板"""
        if self.is_running:
            logger.warning("⚠️ 剪貼板監控已在執行中")
            return
        
        self.is_running = True
        self.last_clipboard = ""
        
        # 建立監控執行緒
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self.monitor_thread.start()
        
        logger.info("✅ 剪貼板監控已啟動")
    
    def stop(self):
        """停止監控剪貼板"""
        self.is_running = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        logger.info("⏹️ 剪貼板監控已停止")
    
    def get_clipboard_content(self) -> str:
        """取得剪貼板內容"""
        try:
            content = pyperclip.paste()
            return content if isinstance(content, str) else ""
        except Exception as e:
            logger.warning(f"⚠️ 獲取剪貼板內容失敗: {e}")
            return ""
    
    def set_clipboard_content(self, content: str):
        """設定剪貼板內容"""
        try:
            pyperclip.copy(content)
            self.last_clipboard = content
            logger.info("✅ 已複製到剪貼板")
        except Exception as e:
            logger.warning(f"⚠️ 設定剪貼板內容失敗: {e}")
    
    def _monitor_loop(self):
        """監控迴圈"""
        while self.is_running:
            try:
                current_clipboard = self.get_clipboard_content()
                
                # 檢查剪貼板內容是否改變
                if current_clipboard != self.last_clipboard:
                    self.last_clipboard = current_clipboard
                    
                    # 呼叫回調函數
                    if self.callback and current_clipboard.strip():
                        try:
                            self.callback(current_clipboard)
                        except Exception as e:
                            logger.error(f"❌ 回調函數執行失敗: {e}")
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"❌ 監控迴圈錯誤: {e}")
                time.sleep(self.check_interval)
