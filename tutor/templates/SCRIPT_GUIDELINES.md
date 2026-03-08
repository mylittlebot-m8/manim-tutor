# Manim 脚本编写规范

## ⚠️ 核心原则：LaTeX 中文支持配置

### 原则 1：必须使用 xelatex 编译器

**原因：**
- xeCJK 需要 xelatex 才能工作
- Manim 默认使用 latex（pdflatex），不支持中文
- 必须显式配置使用 xelatex

**配置方法：**
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
```

### 原则 2：使用 Tex 而不是 MathTex（推荐）

```python
# ✅ 推荐：Tex 支持中文 + 公式混合
Tex(r"顶点坐标：$(1, 4)$", tex_template=template)

# ✅ 也可用：MathTex + \text
MathTex(r"\text{顶点坐标：}(1, 4)", tex_template=template)

# ❌ 错误：未配置 xelatex
MathTex(r"顶点坐标：$(1, 4)$")  # 会报错！
```

### 原则 3：服务端已配置，直接使用模板

**服务端配置（已完成）：**
- ✅ xeCJK 已安装
- ✅ 中文字体已安装（文泉驿正黑）
- ✅ xelatex 编译器可用

**使用模板时会自动配置：**
```python
# 模板中已包含配置
from manim import *

config.tex_compiler = "xelatex"
template = TexTemplate()
template.tex_compiler = "xelatex"
template.output_format = ".xdv"
template.add_to_preamble(r"\usepackage{xeCJK}")
template.add_to_preamble(r"\setCJKmainfont{WenQuanYi Zen Hei}")
```

---

## 🎯 设计原则：学生友好第一

**核心理念：** 所有内容面向学生，确保易懂、清晰、详细

### 详细说明原则

1. **每一步都解释"为什么"**
```python
# ❌ 只说"做什么"
Text("令 y = 0", font_size=24)

# ✅ 说明"为什么"
Text("思路：A、B 是与 x 轴交点", font_size=24, color="#f39c12")
Text("所以 y 坐标为 0", font_size=22, color="#7f8c8d")
Text("令 y = 0，解方程：", font_size=24)
```

2. **不跳步，展示完整推导**
```python
# ❌ 跳步（学生看不懂）
Text("令 y = 0", font_size=24)
MathTex(r"-x^2 + 2x + 3 = 0", font_size=24)
MathTex(r"x = -1, 3", font_size=24)

# ✅ 完整推导（学生能跟上）
Text("步骤 1：令 y = 0", font_size=26)
MathTex(r"-x^2 + 2x + 3 = 0", font_size=24)
Text("步骤 2：整理方程（两边乘以 -1）", font_size=22, color="#95a5a6")
MathTex(r"x^2 - 2x - 3 = 0", font_size=24)
Text("步骤 3：因式分解", font_size=22, color="#95a5a6")
Text("找两个数，乘积为 -3，和为 -2", font_size=20, color="#7f8c8d")
MathTex(r"(x-3)(x+1) = 0", font_size=24, color="#f39c12")
```

3. **关键步骤用颜色/大小突出**
```python
# 标题用大字号 + 主题色
title = Text("第 (1) 问：求 A、B 坐标", font_size=40, color="#3498db")

# 步骤标题用中字号 + 强调色
step_title = Text("步骤 1：令 y = 0", font_size=28, color="#3498db")

# 详细说明用小字号 + 灰色
detail = Text("因为与 x 轴交点，所以 y 坐标为 0", 
             font_size=22, color="#7f8c8d")

# 重点公式用高亮色
formula = MathTex(r"(x-3)(x+1) = 0", font_size=24, color="#f39c12")

# 结论用绿色
conclusion = Text("∴ A(-1, 0), B(3, 0)", font_size=28, color="#2ecc71")
```

4. **每幕结束有小结**
```python
def scene_summary(self):
    """小结场景"""
    title = Text("本问小结", font_size=44, color="#3498db")
    
    # 答案汇总
    answer = VGroup(
        Text("答案：", font_size=32, color="#f39c12"),
        MathTex(r"A(-1, 0)", font_size=28),
        MathTex(r"B(3, 0)", font_size=28)
    ).arrange(DOWN, buff=0.4)
    
    # 方法总结
    method = VGroup(
        Text("解题方法：", font_size=28, color="#f39c12"),
        Text("1. 与 x 轴交点 → 令 y = 0，解方程", font_size=22),
        Text("2. 因式分解 → 找两个数，乘积为 c，和为 b", font_size=22)
    ).arrange(DOWN, buff=0.3)
    
    content = VGroup(title, answer, method).arrange(DOWN, buff=0.5)
```

---

## 📋 字体大小规范

| 内容类型 | 字体大小 | 颜色 | 示例 |
|---------|---------|------|------|
| 主标题 | 40-48px | #3498db（蓝色） | "抛物线综合题" |
| 副标题 | 28-32px | #f39c12（橙色） | "第 (1) 问：求 A、B 坐标" |
| 步骤标题 | 26-28px | #3498db（蓝色） | "步骤 1：令 y = 0" |
| 详细说明 | 20-22px | #7f8c8d（灰色） | "因为与 x 轴交点..." |
| 公式 | 24-28px | WHITE 或 #f39c12 | "-x² + 2x + 3 = 0" |
| 结论 | 28-32px | #2ecc71（绿色） | "∴ A(-1, 0), B(3, 0)" |

---

## ✅ 检查清单

在提交脚本前，请检查：

- [ ] **已配置 xelatex 编译器**
- [ ] **已使用支持中文的 TexTemplate**
- [ ] **Tex/MathTex 已传入 tex_template 参数**
- [ ] 每一步都有"为什么"的说明
- [ ] 没有跳步，推导完整
- [ ] 关键步骤用颜色/大小突出
- [ ] 每幕结束有小结
- [ ] 字体大小符合规范
- [ ] 颜色使用合理（重点内容高亮）
- [ ] 文字详细但不冗长

---

## 📚 参考示例

- `templates/example_student_friendly.py` - 完整学生友好示例
- `templates/script_standard.py` - 标准模板（含 xelatex 配置）
- `STUDENT_FRIENDLY_GUIDE.md` - 学生友好设计指南

---

**遵守这些规则，可以确保脚本在任何环境下都能正常渲染，并且学生易懂！** 🎉
