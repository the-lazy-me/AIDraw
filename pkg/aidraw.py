from typing import Optional, List

from plugins.AIDraw.pkg.core.config_manager import ConfigManager
from .api.api_service import APIService
from .draw.draw_service import DrawService
from .utlis.logger import Logger

class AIDraw:
    """AIDraw主控制器"""
    
    def __init__(self):
        """初始化AIDraw控制器"""
        # 配置管理器
        self.config_manager = ConfigManager()
        
        # 日志工具
        self.logger = Logger(
            config=self.config_manager.config
        )
        
        # 输出初始化信息
        self.logger.debug("调试模式已启用")
        
        # API服务
        self.api_service = APIService(self.config_manager.provider_config_path, self.logger)
        
        # 绘图服务
        baseurl, api_key = self.api_service.get_api_credentials()
        self.draw_service = DrawService(
            baseurl=baseurl,
            api_key=api_key,
            logger=self.logger
        )
        
        self.logger.info("插件 AIDraw 初始化完成")
    
    async def generate_image(self, prompt: str, width: int = None, height: int = None) -> Optional[str]:
        """生成图片
        
        Args:
            prompt: 图片生成提示词
            width: 图片宽度，如果为None则使用配置中的默认值
            height: 图片高度，如果为None则使用配置中的默认值
            
        Returns:
            生成的图片路径，如果失败则返回None
        """
        # 检查绘图服务是否已初始化
        if not self.draw_service:
            self.logger.error("绘图服务尚未初始化")
            return None
        
        # 检查API凭证是否有效
        baseurl, api_key = self.api_service.get_api_credentials()
        if not api_key:
            self.logger.error("未找到有效的API凭证，请检查provider.json配置")
            return None
        
        # 获取配置
        draw_model = self.config_manager.config.get("draw_model", "Daydream")
        
        # 如果未指定宽高，则使用配置中的默认值
        if width is None:
            width = self.config_manager.config.get("image_width", 512)
        if height is None:
            height = self.config_manager.config.get("image_height", 768)
        
        # 生成图片
        self.logger.debug(f"准备生成图片，模型: {draw_model}, 提示词: {prompt}, 宽度: {width}, 高度: {height}")
        try:
            image_url = await self.draw_service.generate_image(
                prompt=prompt,
                model=draw_model,
                width=width,
                height=height
            )
            return image_url
        except Exception as e:
            self.logger.error(f"生成图片时发生异常: {e}")
            return None 