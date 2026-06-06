"""
日誌工具模組
"""

import logging
import os
from datetime import datetime
from pathlib import Path

class Logger:
    """統一的日誌記錄器"""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name):
        """獲取或建立日誌記錄器"""
        if name not in Logger._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            
            # 建立日誌文件夾
            log_dir = Path('logs')
            log_dir.mkdir(exist_ok=True)
            
            # 檔案處理器
            log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
            fh = logging.FileHandler(log_file, encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            
            # 控制台處理器
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            # 格式設定
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            
            logger.addHandler(fh)
            logger.addHandler(ch)
            
            Logger._loggers[name] = logger
        
        return Logger._loggers[name]
