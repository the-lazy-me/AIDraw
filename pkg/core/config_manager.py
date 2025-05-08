import os
import yaml
import shutil
from pathlib import Path

class ConfigManager:
    """配置管理器，负责配置文件的加载、保存和管理"""
    
    def __init__(self):
        # 基础路径
        self.plugin_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.global_config_dir = os.path.join(os.getcwd(), "data", "plugins", "AIDraw")
        
        # 创建目录
        os.makedirs(self.global_config_dir, exist_ok=True)
        
        # 配置文件路径
        self.config_path = os.path.join(self.global_config_dir, "config.yaml")
        self.template_path = os.path.join(os.path.dirname(self.plugin_dir), "templates", "config.yaml.example")
        
        # 提供商配置路径
        self.provider_config_path = "data/config/provider.json"
        
        # 加载配置
        self.config = self.load()
    
    def load(self):
        """加载配置文件"""
        # 如果配置文件不存在，从模板创建
        if not os.path.exists(self.config_path):
            if os.path.exists(self.template_path):
                shutil.copy2(self.template_path, self.config_path)
                print(f"配置文件已从模板创建: {self.config_path}")
            else:
                raise FileNotFoundError(f"错误：配置模板文件 {self.template_path} 不存在，无法创建默认配置")
        
        # 读取配置文件
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            
            return config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            raise
    
    def save(self, config=None):
        """保存配置到文件"""
        if config is None:
            config = self.config
            
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            print(f"配置已保存到: {self.config_path}")
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False 