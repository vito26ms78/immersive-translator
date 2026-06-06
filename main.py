"""
沉浸式英文翻譯軟體 - 主程式入口
Immersive English Translator - Main Entry Point
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.logger import Logger

logger = Logger.get_logger(__name__)

def main():
    """主程式函數"""
    try:
        logger.info("="*60)
        logger.info("沉浸式英文翻譯軟體啟動")
        logger.info("="*60)
        
        # 建立 PyQt6 應用
        app = QApplication(sys.argv)
        app.setApplicationName("沉浸式英文翻譯軟體")
        app.setApplicationVersion("1.0.0")
        
        # 建立主窗口
        main_window = MainWindow()
        main_window.show()
        
        logger.info("主窗口已顯示")
        
        # 執行應用
        sys.exit(app.exec())
        
    except Exception as e:
        logger.critical(f"應用程式啟動失敗: {e}", exc_info=True)
        print(f"❌ 致命錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
