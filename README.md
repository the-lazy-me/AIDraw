# AIDraw 绘图插件

一个简单强大的LangBot AI绘图插件，支持基于提示词生成图片。

## 功能特点

- 使用[启航 AI](https://api.qhaigc.net/) 的高质量绘图模型
- 支持高品质图片生成
- 配置友好，易于使用
- 图片自动保存，方便查看历史生成记录

## 安装方法

配置完成 [LangBot](https://github.com/RockChinQ/LangBot)主程序后使用管理员账号向机器人发送命令即可安装：

```
!plugin get https://github.com/your-username/AIDraw.git
```

## 配置说明

插件首次运行时会在 `data/plugins/AIDraw` 目录下自动创建配置文件 `config.yaml`。这个配置文件是从插件目录下的 `templates/config.yaml.example` 模板复制而来。

配置文件内容如下：

```yaml
# 全局配置文件

# 默认绘图模型
draw_model: Daydream

# 默认图片宽度
image_width: 1024

# 默认图片高度
image_height: 1024

# 调试模式（启用详细日志和临时文件保存）
# 0: 关闭, 1: 开启
aidraw_debug: 0
```

所有的配置信息都集中在这个文件中，您可以根据需要修改相关参数。

### API配置

插件使用 OpenAI 兼容的图像生成 API，需要在 `data/config/provider.json` 中配置：

```json
{
  "requester": {
    "openai-chat-completions": {
      "base-url": "https://api.openai.com/v1"
    }
  },
  "keys": {
    "openai": [
      "your-api-key-here"
    ]
  }
}
```

您可以使用 OpenAI 的 API 或任何兼容 OpenAI API 的第三方服务，如[启航AI](https://api.qhaigc.net/)等。

## 使用方法

### 基本命令

- `/draw <提示词>` - 根据提示词生成图片，可以通过`-w`和`-h`指定宽和高
- `/draw 帮助` - 查看帮助信息

### 绘图示例

```
/draw girl
/draw girl -w 1024
/draw girl -w 1024 -h 1536
/draw 帮助
```

系统将根据提示词生成相应的图片，并发送到当前聊天。

### 注意事项

1. 生成图片质量和效果与提示词质量密切相关，建议提供详细且清晰的描述
2. 部分模型可能有内容限制，某些敏感内容可能会被过滤
3. 图片生成需要一定时间，请耐心等待

## 支持平台

AIDraw 插件支持 LangBot 支持的所有平台。
