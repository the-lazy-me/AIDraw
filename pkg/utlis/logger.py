import os
import datetime

class Logger:
    """AIDraw 日志工具
    
    主要用于记录调试信息和错误信息
    """
    
    def __init__(self, config=None):
        """初始化日志工具
        
        Args:
            config: 配置信息，用于获取调试模式设置
        """
        self.config = config or {}
        self.debug_mode = self.config.get("aidraw_debug", 0) == 1
        
        # 设置日志文件路径
        if self.debug_mode:
            log_dir = os.path.join(os.getcwd(), "data", "plugins", "AIDraw", "logs")
            os.makedirs(log_dir, exist_ok=True)
            self.log_file = os.path.join(log_dir, f"aidraw_log_{datetime.datetime.now().strftime('%Y%m%d')}.log")
        else:
            self.log_file = None
            
    def _write_log(self, level, message):
        """写入日志
        
        Args:
            level: 日志级别，如 INFO, DEBUG, ERROR 等
            message: 日志消息
        """
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{time_str}] [{level}] {message}"
        
        print(log_entry)
        
        if self.debug_mode and self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(log_entry + "\n")
            except Exception as e:
                print(f"无法写入日志文件: {e}")
                
    def info(self, message):
        """记录一般信息
        
        Args:
            message: 日志消息
        """
        self._write_log("INFO", message)
        
    def debug(self, message):
        """记录调试信息，仅在调试模式下记录
        
        Args:
            message: 日志消息
        """
        if self.debug_mode:
            self._write_log("DEBUG", message)
            
    def error(self, message):
        """记录错误信息
        
        Args:
            message: 日志消息
        """
        self._write_log("ERROR", message)
        
    def warning(self, message):
        """记录警告信息
        
        Args:
            message: 日志消息
        """
        self._write_log("WARNING", message) 