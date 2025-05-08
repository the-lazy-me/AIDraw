import os
import base64
import uuid
import aiohttp
from typing import Optional, Dict, Any
from datetime import datetime

class DrawService:
    """绘图服务，负责调用API生成图片"""
    
    def __init__(self, baseurl: str, api_key: str, logger=None):
        """初始化绘图服务
        
        Args:
            baseurl: API服务的基础URL
            api_key: API密钥
            logger: 日志工具实例
        """
        self.baseurl = baseurl
        self.api_key = api_key
        self.logger = logger
    
    async def generate_image(self, prompt: str, model: str = None, 
                             width: int = 512, height: int = 768, 
                             **kwargs) -> Optional[str]:
        """生成图片
        
        Args:
            prompt: 图片生成提示词
            model: 绘图模型，如果为None则使用默认模型
            width: 图片宽度
            height: 图片高度
            **kwargs: 其他参数
            
        Returns:
            生成的图片URL，如果失败则返回None
        """
        # 如果未指定模型，使用默认模型
        if not model:
            model = "Daydream"
        
        try:
            # 直接调用API获取图片URL
            return await self._generate_with_api(prompt, model, width, height, **kwargs)
        except Exception as e:
            if self.logger:
                self.logger.error(f"生成图片时出错: {e}")
            return None
    
    async def _generate_with_api(self, prompt: str, model: str, 
                                width: int, height: int, **kwargs) -> Optional[str]:
        """使用API生成图片
        
        Args:
            prompt: 图片生成提示词
            model: 模型名称
            width: 图片宽度
            height: 图片高度
            **kwargs: 其他参数
            
        Returns:
            生成的图片URL，如果失败则返回None
        """
        try:
            # 检查API凭证
            if not self.api_key:
                if self.logger:
                    self.logger.error("API密钥无效，无法生成图片")
                return None
            
            # 构建API请求
            url = f"{self.baseurl}/images/generations"
            headers = {
                "Authorization": f"{self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 构建请求数据
            data = {
                "model": model,
                "prompt": prompt,
                "size": f"{width}x{height}"
            }
            
            # 添加其他参数
            for key, value in kwargs.items():
                if key not in data:
                    data[key] = value
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        # 处理响应
                        if "data" in response_data and len(response_data["data"]) > 0:
                            image_data = response_data["data"][0]
                            
                            # 响应中包含URL，直接返回
                            if "url" in image_data:
                                img_url = image_data["url"]
                                
                                return img_url
                            
                            # 如果是base64格式，暂不支持直接返回URL
                            elif "b64_json" in image_data:
                                if self.logger:
                                    self.logger.warning("API返回了base64格式的图片，无法提供URL")
                                return None
                    
                    # 如果请求失败
                    error_msg = await response.text()
                    if self.logger:
                        self.logger.error(f"API请求失败: {response.status} - {error_msg}")
            
            return None
        except Exception as e:
            if self.logger:
                self.logger.error(f"生成图片时出错: {e}")
            return None