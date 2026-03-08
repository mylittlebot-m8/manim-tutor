# 项目整理说明

## ✅ 已完成

### 1. Git 配置
- ✅ 创建 `.gitignore` - 屏蔽音频/视频文件
- ✅ 创建 `README.md` - 项目文档
- ✅ 清理 `__MACOSX` 和 `.DS_Store` 文件

### 2. 核心脚本
位于 `tutor_skill/tutor/scripts/`：

**推荐使用：**
- `render_integrated.py` - 集成渲染脚本（远程渲染 + TTS）
- `tts_qwen.py` - Qwen TTS 生成
- `script_with_tts_timing.py` - 带 TTS 同步的脚本模板

**其他工具：**
- `add_subtitles.py` - 添加字幕
- `generate_subtitles.py` - 生成字幕文件
- `check.py` - 检查脚本
- `validate_audio.py` - 验证音频

### 3. 示例项目
位于 `tutor_skill/tutor/projects/`：

**推荐参考：**
- `20260305_002_几何旋转综合题/script_layout_v19.py` - 最新版本（v19）
- `20260303_009_含参抛物线_最终版/script.py` - 抛物线题目

### 4. 模板文件
位于 `tutor_skill/tutor/templates/`：
- `script_scaffold.py` - 基础模板
- `script_example.py` - 示例脚本

---

## 📦 Git 提交策略

### 会提交的文件 ✅
- Python 脚本（*.py）
- 配置文件（*.json, *.md）
- 依赖文件（requirements.txt）
- 文档文件（*.md）

### 不会提交的文件 ❌
- 音频文件（*.wav, *.mp3, audio/）
- 视频文件（*.mp4, *.mov, media/）
- 编译文件（__pycache__/, *.pyc）
- 临时文件（*.tmp, *.log）
- 系统文件（.DS_Store, __MACOSX/）

---

## 🚀 下一步

### 等待 GitHub Token

收到 Token 后，我会：

1. **初始化 Git 仓库**
```bash
cd /Users/wenjigkuai/.openclaw/workspace/tutor_skill
git init
git add .
git commit -m "Initial commit: Manim 数学题解析工具"
```

2. **创建远程仓库**
```bash
# 使用您的 Token
git remote add origin https://mylittlebot-m8:TOKEN@github.com/mylittlebot-m8/manim-tutor.git
```

3. **推送代码**
```bash
git branch -M main
git push -u origin main
```

---

## 📁 项目结构概览

```
tutor_skill/
├── .gitignore              # Git 忽略配置
├── README.md               # 项目文档
├── requirements.txt        # Python 依赖
├── PROMPT_TEMPLATE.md      # 提示词模板
├── PROMPT_TEMPLATE_V2.md   # 提示词模板 V2
└── tutor/
    ├── scripts/            # 脚本工具
    │   ├── render_integrated.py    # ⭐ 集成渲染
    │   ├── tts_qwen.py             # ⭐ TTS 生成
    │   └── ...
    ├── projects/           # 项目文件
    │   ├── 20260305_002_几何旋转综合题/
    │   │   └── script_layout_v19.py  # ⭐ 最新版本
    │   └── ...
    └── templates/          # 模板文件
```

---

## 🎯 核心功能

1. **远程渲染** - 使用 Ubuntu 服务器 GPU 渲染
2. **TTS 集成** - Qwen 语音合成
3. **音频同步** - 自动匹配动画与语音
4. **字幕生成** - ASS 字幕嵌入
5. **批量处理** - 支持多场景批量渲染

---

**准备就绪！等待 GitHub Token 后即可推送代码。** 🎉
