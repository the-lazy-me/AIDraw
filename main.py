from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from pkg.platform.types import *

from .pkg.aidraw import AIDraw
import re

HELP_INFO = "/draw 提示词\n/draw -w 宽度 -h 高度 提示词\n/draw 帮助"

# --- Main Plugin Class ---
@register(name="AIDraw", description="AI 绘图插件，支持多种绘图模型", version="1.0", author="the-lazy-me")
class AIDrawPlugin(BasePlugin):

    def __init__(self, host: APIHost):
        global _aidraw_instance
        super().__init__(host)
        self.aidraw = AIDraw()
        _aidraw_instance = self.aidraw
        
        self.logger = self.aidraw.logger
        self.logger.info("AIDraw 插件已加载")

    @handler(PersonNormalMessageReceived)
    @handler(GroupNormalMessageReceived)
    async def reply_img_message(self, ctx: EventContext):
        msg = ctx.event.text_message
        """
        !draw 提示词
        !draw -w 宽度 -h 高度 提示词
        !draw 帮助
        """
        # 支持！！/draw 提示词
        if msg.startswith("/draw"):
            content = msg[len("/draw"):].strip()
            if content and content != "帮助":
                try:
                    # 解析宽高参数
                    width_match = re.search(r'-w\s+(\d+)', content)
                    height_match = re.search(r'-h\s+(\d+)', content)
                    
                    width = int(width_match.group(1)) if width_match else None
                    height = int(height_match.group(1)) if height_match else None
                    
                    # 移除所有宽高参数，得到纯净的提示词
                    prompt = re.sub(r'-[wh]\s+\d+', '', content).strip()
                    
                    # 如果宽度或高度只指定了一个，需要计算等比例缩放
                    if (width and not height) or (height and not width):
                        # 获取配置中的宽高
                        config_width = self.aidraw.config_manager.config.get("image_width", 512)
                        config_height = self.aidraw.config_manager.config.get("image_height", 768)
                        config_ratio = config_width / config_height
                        
                        # 计算缺失的维度
                        if width and not height:
                            height = int(width / config_ratio)
                        elif height and not width:
                            width = int(height * config_ratio)
                    
                    self.logger.info(f"开始处理绘图请求，提示词: {prompt}, 宽度: {width}, 高度: {height}")
                    image_url = await self.aidraw.generate_image(prompt, width=width, height=height)
                    if image_url:
                        size_info = f" (宽度: {width}, 高度: {height})" if width and height else ""
                        message_elements = MessageChain([Plain(f"[AI绘图] 提示词: {prompt}{size_info}\n"), Image(url=image_url)])
                        await ctx.reply(message_elements)
                    else:
                        await ctx.reply(MessageChain([Plain(f"[AI绘图] 生成图片失败，请检查API配置或稍后重试。")]))
                except Exception as e:
                    self.logger.error(f"绘图过程中发生异常: {e}")
                    await ctx.reply(MessageChain([Plain(f"[AI绘图] 生成图片时出现错误: {str(e)}")]))
            elif content == "帮助" or not content:
                await ctx.reply(MessageChain([Plain(HELP_INFO)]))

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    def __del__(self):
        """插件卸载时执行的清理操作"""
        print("AIDraw 插件已卸载")