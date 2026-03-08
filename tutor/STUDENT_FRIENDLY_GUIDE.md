# 学生友好型脚本设计指南

## 🎯 核心理念

**面对对象是学生，讲解和文字务必详细**

---

## 📋 设计原则

### 原则 1：详细说明每一步的"为什么"

```python
# ❌ 只说"做什么"
Text("令 y = 0", font_size=24)
MathTex(r"y = 0", font_size=24)

# ✅ 说明"为什么"
Text("思路：A、B 是与 x 轴交点", font_size=24, color="#f39c12")
Text("所以 y 坐标为 0", font_size=22, color="#7f8c8d")
Text("令 y = 0，解方程：", font_size=24)
MathTex(r"y = 0", font_size=24)
```

### 原则 2：不跳步，展示完整推导

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
Text("步骤 4：解得 x 的值", font_size=22, color="#95a5a6")
MathTex(r"x_1 = 3, x_2 = -1", font_size=24)
```

### 原则 3：关键步骤用颜色/大小突出

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

### 原则 4：每幕结束有小结

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

## 🎨 字体大小规范

| 内容类型 | 字体大小 | 颜色 | 示例 |
|---------|---------|------|------|
| 主标题 | 40-48px | #3498db（蓝色） | "抛物线综合题" |
| 副标题 | 28-32px | #f39c12（橙色） | "第 (1) 问：求 A、B 坐标" |
| 步骤标题 | 26-28px | #3498db（蓝色） | "步骤 1：令 y = 0" |
| 详细说明 | 20-22px | #7f8c8d（灰色） | "因为与 x 轴交点..." |
| 公式 | 24-28px | WHITE 或 #f39c12 | "-x² + 2x + 3 = 0" |
| 结论 | 28-32px | #2ecc71（绿色） | "∴ A(-1, 0), B(3, 0)" |

---

## 📝 详细讲解模板

### 模板 1：方程求解

```python
def solve_equation(self):
    # 1. 说明思路
    Text("思路：要求与 x 轴交点，令 y = 0", font_size=24, color="#f39c12")
    
    # 2. 列方程
    Text("步骤 1：列方程", font_size=26)
    MathTex(r"-x^2 + 2x + 3 = 0", font_size=24)
    
    # 3. 整理方程（说明每一步）
    Text("步骤 2：整理方程（两边乘以 -1）", font_size=22, color="#95a5a6")
    MathTex(r"x^2 - 2x - 3 = 0", font_size=24)
    
    # 4. 因式分解（提示方法）
    Text("步骤 3：因式分解", font_size=22, color="#95a5a6")
    Text("找两个数，乘积为 -3，和为 -2", font_size=20, color="#7f8c8d")
    MathTex(r"(x-3)(x+1) = 0", font_size=24, color="#f39c12")
    
    # 5. 求解
    Text("步骤 4：解得 x 的值", font_size=22, color="#95a5a6")
    MathTex(r"x_1 = 3, x_2 = -1", font_size=24)
    
    # 6. 结论
    Text("∴ 与 x 轴交点为 A(-1, 0), B(3, 0)", font_size=28, color="#2ecc71")
```

### 模板 2：几何证明

```python
def prove_geometry(self):
    # 1. 已知条件
    Text("已知：", font_size=28, color="#f39c12")
    MathTex(r"AB = 5, \\angle ABC = 90^\\circ", font_size=24)
    
    # 2. 求证目标
    Text("求证：", font_size=28, color="#f39c12")
    MathTex(r"AC^2 = AB^2 + BC^2", font_size=24)
    
    # 3. 证明过程（详细）
    Text("证明：", font_size=28, color="#3498db")
    Text("根据勾股定理，在直角三角形 ABC 中：", font_size=22)
    MathTex(r"AC^2 = AB^2 + BC^2", font_size=24)
    
    # 4. 代入数值
    Text("代入 AB = 5, BC = 3：", font_size=22, color="#95a5a6")
    MathTex(r"AC^2 = 5^2 + 3^2 = 25 + 9 = 34", font_size=24)
    
    # 5. 结论
    Text("∴ AC² = AB² + BC² 得证", font_size=28, color="#2ecc71")
```

### 模板 3：函数分析

```python
def analyze_function(self):
    # 1. 函数表达式
    Text("已知函数：", font_size=28, color="#3498db")
    MathTex(r"f(x) = ax^2 + bx + c", font_size=28)
    
    # 2. 顶点公式推导
    Text("顶点横坐标公式：", font_size=26)
    Text("推导：对称轴是 x = -b/(2a)", font_size=22, color="#7f8c8d")
    MathTex(r"x = -\frac{b}{2a}", font_size=26)
    
    # 3. 代入求值
    Text("代入 a = -1, b = 2：", font_size=22, color="#95a5a6")
    MathTex(r"x = -\frac{2}{2\\cdot(-1)} = 1", font_size=26)
    
    # 4. 求纵坐标
    Text("将 x = 1 代入原函数求 y：", font_size=22, color="#95a5a6")
    MathTex(r"y = -1^2 + 2\\cdot 1 + 3 = 4", font_size=26)
    
    # 5. 结论
    Text("∴ 顶点坐标为 (1, 4)", font_size=28, color="#2ecc71")
```

---

## ✅ 检查清单

在提交脚本前，请检查：

- [ ] 每一步都有"为什么"的说明
- [ ] 没有跳步，推导完整
- [ ] 关键步骤用颜色/大小突出
- [ ] 每幕结束有小结
- [ ] 字体大小符合规范
- [ ] 颜色使用合理（重点内容高亮）
- [ ] 文字详细但不冗长
- [ ] 公式与中文分离（遵循 SCRIPT_GUIDELINES.md）

---

## 📚 参考示例

- `templates/example_student_friendly.py` - 完整学生友好示例
- `templates/script_standard.py` - 标准模板（支持详细讲解）
- `templates/SCRIPT_GUIDELINES.md` - 公式与中文分离规范

---

## 💡 常见问题

### Q: 详细说明会不会太冗长？

**A:** 详细≠冗长。关键是：
- 解释"为什么"（思路）
- 展示"怎么做"（步骤）
- 提示"注意什么"（关键点）

### Q: 如何平衡详细和简洁？

**A:** 根据目标学生水平调整：
- 初学者：更详细，每步解释
- 进阶学生：适当精简，重点讲解

### Q: 颜色太多会不会分散注意力？

**A:** 遵循"少即是多"原则：
- 主题色（蓝色）：标题、步骤
- 强调色（橙色）：重点公式
- 成功色（绿色）：结论
- 灰色：辅助说明

---

**记住：我们的目标是让学生真正理解，而不是仅仅展示答案！** 🎉
