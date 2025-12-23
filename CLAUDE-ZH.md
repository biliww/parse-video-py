# CLAUDE-ZH.md

本文档为 Claude Code (claude.ai/code) 在处理此仓库代码时提供指导。

## 项目概述

这是一个基于 Python 的视频解析服务，可以从多个中国社交媒体平台提取视频信息。它能够去除水印并提供来自 20 多个平台的直接视频 URL，包括抖音、快手、微博、小红书等。

## 架构

应用程序采用模块化架构：

- **FastAPI Web 框架** ([`main.py`](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/main.py)): 提供 REST API 端点和 Web 界面
- **解析器模块** ([`parser/`](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser)): 包含具有通用基类的平台特定解析器
- **模板系统** ([`templates/`](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/templates)): 用于 Web 界面的 Jinja2 模板
- **工具函数** ([`utils/`](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/utils)): 共享的工具函数

### 核心组件

**BaseParser 系统** ([`parser/base.py`](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py)):
- 定义所有平台解析器接口的抽象基类
- 使用 fake-useragent 提供通用头部信息
- 定义数据结构：`VideoInfo`、`VideoAuthor`、`ImgInfo`

**平台解析器** ([`parser/`](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser)):
每个平台都有继承自 [BaseParser](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L28-L141) 的独立解析器：
- 必须实现 [parse_share_url()](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L63-L63) 和 [parse_video_id()](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L64-L64) 方法
- 返回标准化的 [VideoInfo](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L109-L118) 对象
- 某些解析器支持视频和图像相册解析（例如微博、抖音、快手）
- 图像 URL 存储在 [images](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L117-L117) 字段中作为 [ImgInfo](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L125-L129) 对象

**视频源映射** ([`parser/__init__.py`](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/__init__.py)):
- 将 [VideoSource](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L15-L25) 枚举映射到域名列表和解析器类
- 包含 [video_source_info_mapping](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/__init__.py#L12-L46) 字典用于路由请求
- 提供 [parse_video_share_url()](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/__init__.py#L66-L85) 和 [parse_video_id()](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/__init__.py#L87-L104) 辅助函数

## 开发命令

### 本地开发
```bash
# 创建并激活虚拟环境（需要 Python >= 3.10）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn main:app --reload

# 运行生产服务器
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 代码质量
项目使用带有格式化工具的预提交钩子：
- **Black**: 代码格式化（行长度：88）
- **isort**: 导入排序（black 兼容配置文件）
- **flake8**: 代码检查（最大行长度：88）

```bash
# 安装预提交钩子
pre-commit install

# 手动运行格式化工具
black .
isort .
flake8 .
```

**注意**: `.pre-commit-config.yaml` 中的实际 flake8 配置显示最大行长度为 88，但某些开发使用 79。请遵循每个文件中的现有模式。

### 测试
项目使用 pytest 进行全面的测试覆盖：

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_api.py
pytest tests/test_base.py
pytest tests/test_routing.py
pytest tests/test_weibo_album.py

# 运行测试并显示覆盖率
pytest --cov=parser

# 运行测试并显示详细输出
pytest -v

# 运行特定测试类或方法
pytest tests/test_base.py::TestDataClasses
pytest tests/test_base.py::TestDataClasses::test_video_author_creation

# 运行带有标记的测试
pytest -m unit          # 仅运行单元测试
pytest -m integration   # 仅运行集成测试
pytest -m "not slow"     # 跳过慢速测试
```

**测试结构**: 请参阅 `tests/README.md` 获取详细的测试指南，包括模拟策略和异步测试模式。

### Docker
```bash
# 构建并运行
docker run -d -p 8000:8000 wujunwei928/parse-video-py

# 使用基本身份验证运行
docker run -d -p 8000:8000 -e PARSE_VIDEO_USERNAME=username -e PARSE_VIDEO_PASSWORD=password wujunwei928/parse-video-py
```

## API 使用

### 端点
- `GET /`: Web 界面
- `GET /video/share/url/parse?url=<share_url>`: 从分享 URL 解析视频
- `GET /video/id/parse?source=<source>&video_id=<id>`: 通过 ID 解析视频

### 基本身份验证
设置环境变量以启用身份验证：
```bash
export PARSE_VIDEO_USERNAME=username
export PARSE_VIDEO_PASSWORD=password
```

## 添加新平台

1. 在 [`parser/`](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser) 中创建继承自 [BaseParser](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L28-L141) 的新解析器类
2. 向 [base.py](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py) 中的 [VideoSource](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L15-L25) 枚举添加值
3. 在 [__init__.py](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/__init__.py) 中使用域名和解析器更新 [video_source_info_mapping](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/__init__.py#L12-L46)
4. 实现必需的抽象方法：[parse_share_url()](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L63-L63) 和 [parse_video_id()](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L64-L64)

## 视频数据结构

```python
@dataclasses.dataclass
class VideoInfo:
    video_url: str           # 直接视频 URL
    cover_url: str           # 视频缩略图
    title: str = ""          # 视频标题
    music_url: str = ""      # 背景音乐 URL
    images: List[ImgInfo] = []  # 图像相册 URL
    author: VideoAuthor = VideoAuthor()  # 作者信息
```

## MCP 支持

项目支持 [MCP（模型上下文协议）](https://modelcontextprotocol.io/) 与 AI 工具集成：
- MCP 端点：`http://localhost:8000/mcp`
- 使用 StreamableHttp 方法进行 AI 工具集成
- 通过 [main.py](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/main.py) 中的 FastAPI-MCP 集成启用

## 重要说明

- 所有解析器必须处理分享 URL 和视频 ID
- 使用 `fake_useragent.UserAgent(os=["ios"]).random` 获取移动用户代理
- 视频 URL 应尽可能直接且无水印
- 错误处理应为不支持的平台返回有意义的消息
- 系统支持视频和图像相册解析：
  - 视频内容：存储在 [video_url](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L110-L110) 字段中
  - 图像相册：作为 [ImgInfo](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L125-L129) 对象列表存储在 [images](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L117-L117) 字段中
- 某些平台（微博、抖音、快手、小红书、皮皮虾）支持视频和图像解析
- 哔哩哔哩解析器支持 Cookie 配置以获取更高质量的视频（默认已注释）
- 尽可能使用应用分享链接，桌面网页版本可能未完全测试
- 图像解析器应优先选择最高质量的 URL：large > original > bmiddle > url

## 平台特定实现细节

**抖音 Live Photo 支持**:
- 实现专门的 slidesinfo API 用于带有 Live Photos 的图像相册
- 通过规范 URL 和 HTML 模式检测笔记内容
- 提取静态图像和 Live Photo 视频 URL
- 优先选择非 WebP 图像格式以获得更好的质量
- 支持 jingxuan 页面 URL 的 modal_id 参数
- 生成 API 调用所需的 web_id 和 a_bogus 参数

**微博相册解析**:
- 处理 TV 节目 URL 和常规帖子 URL
- 支持多质量级别的图像相册
- 提取作者信息和时间戳
- 处理不同的 URL 模式：`/tv/show/`、`show?fid=`、常规帖子

## 解析器实现模式

**对于支持视频和图像内容的平台：**
- URL 路由逻辑应检测内容类型并适当路由
- 视频 URL 通常包含 `/tv/show/`、`show?fid=`、`/video/` 等模式
- 图像相册 URL 通常是常规帖子 URL，需要解析以确定内容类型
- 实现回退策略（移动 API → 桌面 HTML 解析）以增强健壮性

**对于图像相册解析：**
- 从平台特定的 API 响应或 HTML 中提取图像 URL
- 在 [images](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L117-L117) 字段中返回多个 [ImgInfo](file:///Users/wangpenglong/projects/PythonProject/parse-video-py/parser/base.py#L125-L129) 对象
- 在适用时处理 LivePhoto 支持（例如抖音、小红书）
- 对于抖音：使用适当的认证参数调用 slidesinfo API
- 对于小红书：从图像元数据中提取 LivePhoto URL

## 直接解析器使用

```python
import asyncio
from parser import parse_video_share_url, parse_video_id, VideoSource

# 从分享 URL 解析
video_info = asyncio.run(parse_video_share_url("share_url"))

# 从视频 ID 解析
video_info = asyncio.run(parse_video_id(VideoSource.DouYin, "video_id"))

# 示例：使用真实 URL 测试解析
```

## 开发和测试

### 认证和安全
- 可通过环境变量启用基本身份验证：`PARSE_VIDEO_USERNAME` 和 `PARSE_VIDEO_PASSWORD`
- 使用 `secrets.compare_digest()` 进行安全的凭据比较
- MCP 集成支持 AI 工具连接到 `/mcp` 端点

### 支持的平台总结
- **视频**: 20 多个平台，包括抖音、快手、微博、哔哩哔哩等
- **图像相册**: 5 个平台（抖音、快手、小红书、皮皮虾、微博）
- **Live Photos**: 抖音和小红书（具有平台特定实现）