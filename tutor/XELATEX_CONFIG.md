# xelatex 中文支持配置说明

## ✅ 服务端配置（已完成）

### 已安装组件

1. **xeCJK 包**
   - 位置：`/usr/share/texlive/texmf-dist/tex/xelatex/xecjk/xeCJK.sty`
   - 功能：支持 XeLaTeX 排版中文

2. **中文字体**
   - 文泉驿正黑：`/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`
   - 文泉驿微米黑：`/usr/share/fonts/truetype/wqy/wqy-microhei.ttc`

3. **xelatex 编译器**
   - 已包含在 texlive-xetex 包中
   - 支持中文排版

---

## 🔧 脚本配置方法

### 方法 1：使用标准模板（推荐）

```python
from manim import *
from templates.script_standard import StandardTeachingScene, template

class MyProblem(StandardTeachingScene):
    def construct(self):
        super().construct()
        # 直接使用，模板已配置好 xelatex
```

### 方法 2：手动配置

```python
from manim import *

# 关键配置：使用 xelatex 编译器
config.tex_compiler = "xelatex"

# 创建支持中文的 TexTemplate
template = TexTemplate()
template.tex_compiler = "xelatex"
template.output_format = ".xdv"  # xelatex 输出 .xdv 格式
template.add_to_preamble(r"\usepackage{xeCJK}")
template.add_to_preamble(r"\setCJKmainfont{WenQuanYi Zen Hei}")

class TestChinese(Scene):
    def construct(self):
        # 使用 Tex（支持中文 + 公式混合）
        text1 = Tex(r"顶点坐标：$(1, 4)$", tex_template=template)
        
        # 或使用 MathTex + \text
        text2 = MathTex(r"\text{顶点坐标：}(1, 4)", tex_template=template)
        
        self.add(text1, text2)
```

---

## 📋 使用规范

### ✅ 正确用法

```python
# 1. Tex 支持中文 + 公式混合
Tex(r"顶点坐标：$(1, 4)$", tex_template=template)

# 2. MathTex + \text
MathTex(r"\text{顶点坐标：}(1, 4)", tex_template=template)

# 3. 纯公式（也建议使用 template）
MathTex(r"x = -\frac{b}{2a}", tex_template=template)
```

### ❌ 错误用法

```python
# 1. 未配置 xelatex
MathTex(r"顶点坐标：$(1, 4)$")  # 会报错！

# 2. 未传入 tex_template
Tex(r"顶点坐标：$(1, 4)$")  # 会报错！

# 3. 使用默认的 MathTex
MathTex(r"\text{中文}")  # 需要 tex_template 参数
```

---

## 🎯 最佳实践

### 1. 优先使用 Tex

```python
# ✅ 推荐：Tex 更简洁
Tex(r"令 $y = 0$，解得 $x = -1, 3$", tex_template=template)

# 也可用：MathTex + \text
MathTex(r"\text{令 } y = 0 \text{，解得 } x = -1, 3", tex_template=template)
```

### 2. 公式与中文分离（可选）

如果 Tex 渲染有问题，可以分离显示：

```python
VGroup(
    Text("顶点坐标：", font_size=24),
    MathTex(r"(1, 4)", font_size=24, tex_template=template)
).arrange(RIGHT, buff=0.2)
```

### 3. 使用标准模板

```python
from templates.script_standard import StandardTeachingScene

class MyProblem(StandardTeachingScene):
    def construct(self):
        super().construct()
        # 所有方法都已配置好 xelatex
        self.create_formula(r"x = -\frac{b}{2a}")  # 自动使用 template
```

---

## 🔍 故障排除

### 问题 1：'NoneType' object has no attribute 'exists'

**原因：** `_find_audio_dir()` 返回 None

**解决：**
```python
# 确保音频目录存在
self.audio_dir = Path(__file__).parent / "audio"
if not self.audio_dir.exists():
    self.audio_dir = Path(__file__).parent.parent / "audio"
```

### 问题 2：LaTeX error converting to dvi

**原因：** 未配置 xelatex 编译器

**解决：**
```python
config.tex_compiler = "xelatex"
template = TexTemplate()
template.tex_compiler = "xelatex"
template.output_format = ".xdv"
```

### 问题 3：中文显示为方框

**原因：** 未配置中文字体

**解决：**
```python
template.add_to_preamble(r"\setCJKmainfont{WenQuanYi Zen Hei}")
```

---

## 📚 参考资源

- `templates/script_standard.py` - 标准模板（含 xelatex 配置）
- `templates/SCRIPT_GUIDELINES.md` - 脚本编写规范
- `STUDENT_FRIENDLY_GUIDE.md` - 学生友好设计指南

---

**配置好 xelatex 后，可以直接在公式中使用中文，无需手动分离！** 🎉
