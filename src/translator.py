"""
Google 翻譯核心模組 - 英文 → 繁體中文
"""

import requests
from typing import Optional
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)

class GoogleTranslator:
    """Google 翻譯引擎 - 專用英文翻譯"""
    
    BASE_URL = "https://translate.google.com/translate_a/single"
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def translate(self, text: str, target_lang: str = 'zh-TW') -> Optional[str]:
        """
        翻譯英文文本
        
        Args:
            text: 英文文本
            target_lang: 目標語言代碼 (預設: zh-TW - 繁體中文)
        
        Returns:
            翻譯結果或 None
        """
        if not text or not text.strip():
            return ""
        
        try:
            params = {
                'client': 'gtx',
                'sl': 'en',  # 固定為英文
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # 解析回應
            data = response.json()
            if data and len(data) > 0 and len(data[0]) > 0:
                translated = ''.join([item[0] for item in data[0] if item[0]])
                logger.info(f"✅ 翻譯成功: {len(text)} 字符 → {len(translated)} 字符")
                return translated
            
            return None
            
        except requests.exceptions.Timeout:
            logger.error("❌ API 超時 - 請檢查網路連接")
            return None
        except requests.exceptions.ConnectionError:
            logger.error("❌ 網路連接失敗")
            return None
        except Exception as e:
            logger.error(f"❌ 翻譯失敗: {e}")
            return None
    
    def translate_batch(self, texts: list) -> dict:
        """
        批量翻譯（提高效率）
        
        Args:
            texts: 文本列表
        
        Returns:
            {原文: 翻譯} 字典
        """
        results = {}
        for text in texts:
            translated = self.translate(text)
            results[text] = translated
        return results
