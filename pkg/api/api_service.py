import json
import os
from typing import List, Tuple, Dict, Optional
import aiohttp
import json

class APIService:
    """API服务，用于与绘图API交互"""
    
    def __init__(self, provider_config_path: str, logger=None):
        """初始化API服务
        
        Args:
            provider_config_path: 提供商配置文件路径
            logger: 日志工具实例
        """
        self.provider_config_path = provider_config_path
        self.logger = logger
    
    def get_api_credentials(self) -> Tuple[str, str]:
        """从provider.json中获取API凭证
        
        Returns:
            包含base_url和api_key的元组
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(self.provider_config_path):
                if self.logger:
                    self.logger.error(f"provider.json 配置文件不存在: {self.provider_config_path}")
                return "https://api.qhaigc.net/v1", ""
            
            # 读取provider.json
            with open(self.provider_config_path, 'r', encoding='utf-8') as f:
                provider_config = json.load(f)
            
            # 提取baseurl和api_key
            base_url = provider_config.get("requester", {}).get("openai-chat-completions", {}).get("base-url", "")
            api_keys = provider_config.get("keys", {}).get("openai", [])
            api_key = api_keys[0] if api_keys else ""
            
            if not base_url:
                if self.logger:
                    self.logger.error("无法从provider.json获取有效的base-url")
                base_url = "https://api.qhaigc.net/v1"
            
            if not api_key:
                if self.logger:
                    self.logger.error("无法从provider.json获取有效的API密钥")
                
            return base_url, api_key
        except Exception as e:
            if self.logger:
                self.logger.error(f"获取API凭证时出错: {e}")
            return "https://api.qhaigc.net/v1", ""
    
    def get_draw_models(self) -> List[str]:
        """获取支持的绘图模型列表
        
        Returns:
            绘图模型ID列表
        """
        return self.draw_models 