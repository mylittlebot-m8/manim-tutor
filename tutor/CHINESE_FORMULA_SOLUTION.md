# 公式不支持中文问题 - 根源解决方案

## 🎯 问题根源

**LaTeX 引擎限制：**
- Manim 使用 LaTeX 渲染 MathTex
- 默认 LaTeX 不支持中文字符
- 即使安装了 xeCJK，配置复杂且兼容性差

---

## ✅ 解决方案：公式与中文分离

### 核心原则

```
MathTex → 纯数学公式（无中文）
Text    → 中文说明（无 LaTeX）
两者配合 → 完整表达
```

### 实施方法

#### 方法 1：Skill 基础规则（推荐）

**在脚本模板中强制执行：**

1. **模板约束** - 使用标准模板 `script_standard.py`
2. **代码审查** - 提交前检查 MathTex 中是否有中文
3. **自动化检查** - 添加 lint 规则

**检查脚本：**
```python
# check_chinese_in_latex.py
import re

def check_script(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 MathTex 中的中文字符
    latex_pattern = r'MathTex\(r?"([^"]+)"'
    matches = re.findall(latex_pattern, content)
    
    for match in matches:
        if re.search(r'[\u4e00-\u9fff]', match):
            print(f"❌ MathTex 中包含中文：{match}")
            return False
    
    print("✅ 检查通过")
    return True
```

#### 方法 2：定义标准方式

**统一使用以下模式：**

```python
# ✅ 标准模式
VGroup(
    Text("中文说明：", font_size=24),
    MathTex(r"纯公式", font_size=24)
).arrange(DOWN, buff=0.3)

# ✅ 步骤模式
Text("步骤 1：令 y = 0", font_size=24)
MathTex(r"y = 0", font_size=24)

# ✅ 结果模式
Text("∴ A(-1, 0), B(3, 0)", font_size=28, color="#2ecc71")
```

---

## 📋 实施清单

### 阶段 1：模板更新

- [x] 创建标准模板 `script_standard.py`
- [x] 创建编写规范 `SCRIPT_GUIDELINES.md`
- [ ] 更新所有现有模板
- [ ] 添加自动化检查脚本

### 阶段 2：培训与文档

- [x] 编写详细规则文档
- [x] 提供正确/错误示例
- [ ] 制作视频教程
- [ ] 建立常见问题 FAQ

### 阶段 3：工具支持

- [ ] IDE 插件（自动提示）
- [ ] CI/CD 检查（提交前验证）
- [ ] 代码高亮规则（中文标红）

---

## 🎨 最佳实践示例

### 示例 1：方程求解

```python
# ❌ 错误：MathTex 包含中文
MathTex(r"\text{令 } y = 0", font_size=24)

# ✅ 正确：Text + MathTex 分离
Text("令 y = 0：", font_size=24)
MathTex(r"y = 0", font_size=24)
```

### 示例 2：几何证明

```python
# ❌ 错误
MathTex(r"\text{顶点坐标：}(1, 4)")

# ✅ 正确
VGroup(
    Text("顶点坐标：", font_size=24),
    MathTex(r"(1, 4)", font_size=24)
).arrange(RIGHT, buff=0.2)
```

### 示例 3：函数分析

```python
# ❌ 错误
MathTex(r"\text{对称轴：} x = -\frac{b}{2a}")

# ✅ 正确
VGroup(
    Text("对称轴：", font_size=24),
    MathTex(r"x = -\frac{b}{2a}", font_size=24)
).arrange(DOWN, buff=0.3)
```

---

## 🚀 快速参考卡片

### MathTex 允许的内容

| 类型 | 示例 |
|------|------|
| 变量 | `x`, `y`, `a`, `b`, `m` |
| 运算符 | `+`, `-`, `=`, `\times`, `\div` |
| 分数 | `\frac{a}{b}` |
| 根号 | `\sqrt{x}`, `\sqrt[n]{x}` |
| 指数 | `x^2`, `x^{n+1}` |
| 希腊字母 | `\alpha`, `\beta`, `\Delta` |
| 函数 | `\sin`, `\cos`, `\log`, `\ln` |
| 几何 | `\angle`, `\triangle`, `\odot` |
| 关系 | `=`, `\neq`, `\approx`, `\equiv` |

### Text 允许的内容

| 类型 | 示例 |
|------|------|
| 中文标题 | "第 (1) 问：求顶点坐标" |
| 步骤说明 | "步骤 1：令 y = 0" |
| 结论 | "∴ A(-1, 0), B(3, 0)" |
| 单位 | "平方厘米", "米/秒" |
| 标点 | "：", "。", "，" |

---

## 📚 相关资源

1. **模板文件**
   - `templates/script_standard.py` - 标准模板
   - `templates/SCRIPT_GUIDELINES.md` - 编写规范

2. **检查工具**
   - `scripts/check_chinese_in_latex.py` - 自动化检查

3. **参考文档**
   - [LaTeX 数学公式符号表](https://artofproblemsolving.com/wiki/index.php/LaTeX:Symbols)
   - [Manim Text 文档](https://docs.manim.community/)

---

## 💡 常见问题

### Q: 如何在公式中显示"度"符号？

```python
# ✅ 使用 LaTeX 的度数符号
MathTex(r"\angle ABC = 90^\circ", font_size=24)
```

### Q: 如何显示"所以"符号？

```python
# ✅ 使用 Unicode 符号
Text("∴ x = 3", font_size=24)

# 或分离显示
Text("∴", font_size=24)
MathTex(r"x = 3", font_size=24)
```

### Q: 如何在公式中显示中文单位？

```python
# ✅ 分离显示
MathTex(r"S = 25", font_size=24)
Text("平方厘米", font_size=24)
```

### Q: 如何显示百分比？

```python
# ✅ 使用 LaTeX 的百分号
MathTex(r"50\%", font_size=24)

# 或分离
MathTex(r"50", font_size=24)
Text("%", font_size=24)
```

---

## ✅ 总结

**从根源上解决公式不支持中文的问题：**

1. **规则约束** - MathTex 只显示纯公式
2. **模板支持** - 使用标准模板自动分离
3. **工具检查** - 提交前自动验证
4. **培训文档** - 让所有开发者了解规则

**遵守这些规则，可以确保脚本在任何环境下都能正常渲染！** 🎉
