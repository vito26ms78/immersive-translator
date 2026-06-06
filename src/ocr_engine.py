"""
OCR 螢幕取字模組
"""

import cv2
import numpy as np
from PIL import ImageGrab
from typing import Optional
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)

class OCREngine:
    """OCR 引擎 - 螢幕文字識別"""
    
    def __init__(self):
        """初始化 OCR 引擎"""
        try:
            import easyocr
            self.reader = easyocr.Reader(['ch_sim', 'ch_tra', 'en'], gpu=False)
            self.available = True
            logger.info("✅ OCR 引擎初始化成功")
        except Exception as e:
            logger.warning(f"⚠️ OCR 引擎初始化失敗: {e}")
            self.available = False
            self.reader = None
    
    def is_available(self) -> bool:
        """檢查 OCR 是否可用"""
        return self.available
    
    def recognize_from_screen(self, x1: int, y1: int, 
                              x2: int, y2: int) -> Optional[str]:
        """
        直接從螢幕區域識別英文文字
        
        Args:
            x1, y1: 起始坐標
            x2, y2: 結束坐標
        
        Returns:
            識別到的英文文字或 None
        """
        if not self.available:
            logger.warning("⚠️ OCR 引擎不可用")
            return None
        
        try:
            # 確保坐標正確
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            
            # 擷取螢幕區域
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            img_array = np.array(screenshot)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # 圖像預處理
            img_bgr = self._preprocess_image(img_bgr)
            
            # 進行 OCR 識別
            results = self.reader.readtext(img_bgr, detail=0)
            text = '\n'.join(results) if results else ""
            
            if text:
                logger.info(f"✅ OCR 識別成功，文字長度: {len(text)}")
            else:
                logger.info("⚠️ OCR 未識別到文字")
            
            return text
            
        except Exception as e:
            logger.error(f"❌ OCR 識別失敗: {e}")
            return None
    
    @staticmethod
    def _preprocess_image(image: np.ndarray) -> np.ndarray:
        """圖像預處理 - 提高識別準確度"""
        try:
            # 灰度化
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 二值化
            _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # 去噪
            denoised = cv2.fastNlMeansDenoising(binary, h=10)
            
            return denoised
            
        except Exception as e:
            logger.warning(f"⚠️ 圖像預處理失敗: {e}，使用原始圖像")
            return image
