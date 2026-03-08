# Manim 数学题解析工具

基于 Manim 的数学题视频生成工具，支持几何题、代数题等数学题目的自动化视频生成。

## 📁 项目结构

```
tutor_skill/
├── tutor/                      # 核心代码
│   ├── scripts/                # 脚本工具
│   │   ├── render_integrated.py    # 集成渲染脚本（推荐）
│   │   ├── tts_qwen.py             # Qwen TTS 生成
│   │   └── script_with_tts_timing.py  # 带 TTS 同步的脚本模板
│   ├── projects/               # 项目文件
│   │   ├── 20260305_002_几何旋转综合题/
│   │   └── ...
│   └── templates/              # 模板文件
├── .gitignore                  # Git 忽略配置
└── requirements.txt            # Python 依赖
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置远程渲染服务

编辑 `tutor/scripts/render_integrated.py`：

```python
REMOTE_SERVICE_URL = "http://117.50.190.204:8000"
API_KEY = "sk-your-api-key"
```

### 3. 创建项目

```bash
cd tutor/projects
mkdir 20260305_003_你的题目
cd 20260305_003_你的题目
cp ../../templates/script_with_tts_timing.py script.py
```

### 4. 编写脚本

参考 `projects/20260305_002_几何旋转综合题/script_layout_v19.py`

### 5. 渲染视频

```bash
source ../../.venv/bin/activate
python ../../scripts/render_integrated.py -p . -q h
```

## 📝 脚本模板

### 基本结构

```python
from manim import *
from pathlib import Path

class YourProblem(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 加载音频配置
        self.audio_dir = Path(__file__).parent / "audio"
        self.audio_timings = self.load_audio_timings()
        
        # 创建内容
        self.scene_1_intro()
        self.scene_2_solution()
        # ...
    
    def load_audio_timings(self):
        # 加载音频时长配置
        pass
    
    def wait_for_audio(self, scene_num, animation_duration=0):
        # 等待音频播放
        pass
    
    def scene_1_intro(self):
        # 第 1 幕内容
        pass
```

## 🎬 布局配置

### 标题位置
```python
self.TITLE_POS = LEFT * 3.85 + UP * 3.567  # 往右 5%
```

### 公式区域
```python
self.FORMULA_START_POS = RIGHT * 0.25 + UP * 0.875  # 往下 15%
```

### 字体大小
- 小号：28
- 中号：32
- 大号：36

### 间距
- 小间距：0.45
- 中间距：0.55

## 🔧 远程渲染服务

### 服务端点

- `POST /render` - 提交渲染任务
- `GET /task/{id}` - 查询任务状态
- `GET /download/{id}` - 下载视频
- `POST /tts/batch` - 批量生成 TTS

### 服务地址

- 主服务：`http://117.50.190.204:8000`
- 备用服务：`http://117.50.91.193:8000`

## 📦 依赖

主要依赖：
- `manim` - 动画引擎
- `dashscope` - Qwen TTS
- `librosa` - 音频分析
- `requests` - HTTP 请求

完整依赖见 `requirements.txt`

## 📚 示例项目

### 几何旋转综合题
位置：`projects/20260305_002_几何旋转综合题/`

包含：
- 完整脚本（v19 版本）
- TTS 音频文件
- 渲染配置

### 含参抛物线
位置：`projects/20260303_009_含参抛物线_最终版/`

包含：
- 抛物线题目解析
- 动态图像演示

## ⚠️ 注意事项

### Git 提交

本项目已配置 `.gitignore`，以下文件**不会**被提交：

- ❌ 音频文件（*.wav, *.mp3, audio/）
- ❌ 视频文件（*.mp4, *.mov, media/）
- ❌ 编译文件（__pycache__/, *.pyc）
- ❌ 临时文件（*.tmp, *.log）

**请仅提交：**
- ✅ Python 脚本（*.py）
- ✅ 配置文件（*.json, *.md）
- ✅ 依赖文件（requirements.txt）

### 音频同步

使用 `wait_for_audio(scene_num, animation_duration)` 确保动画与 TTS 同步。

### 中文字体

使用 xelatex 编译，配置 WenQuanYi Zen Hei 字体：

```python
config.tex_compiler = "xelatex"
template.add_to_preamble(r"\usepackage{xeCJK}")
template.add_to_preamble(r"\setCJKmainfont{WenQuanYi Zen Hei}")
```

## 🤝 贡献

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

---

**开发团队**: MyLittleBot
**最后更新**: 2026-03-09
