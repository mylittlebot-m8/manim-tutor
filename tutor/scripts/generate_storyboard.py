#!/usr/bin/env python3
"""
自动生成带题目读白的分镜脚本

使用方法:
    python scripts/generate_storyboard.py --problem "题目文本" --output storyboard.md
    
示例:
    python scripts/generate_storyboard.py \\
        --problem "已知采购20个萌系公仔和30个喜庆公仔共需2100元..." \\
        --analysis "数学分析内容" \\
        -o storyboard.md
"""

import argparse
import re
from pathlib import Path
from datetime import datetime


def generate_storyboard(problem_text: str, analysis_text: str = "", title: str = "") -> str:
    """
    生成分镜脚本，第一幕为题目朗读
    
    Args:
        problem_text: 完整题目文本
        analysis_text: 数学分析（可选）
        title: 视频标题（可选）
    
    Returns:
        分镜脚本Markdown内容
    """
    
    # 提取标题（如果没有提供）
    if not title:
        # 尝试从题目中提取关键信息
        if "萌系" in problem_text and "喜庆" in problem_text:
            title = "文创店采购问题"
        elif "抛物线" in problem_text:
            title = "抛物线综合题"
        elif "三角形" in problem_text:
            title = "三角形问题"
        else:
            title = "数学应用题解析"
    
    # 清理题目文本（去除多余空格和换行）
    problem_clean = re.sub(r'\s+', ' ', problem_text).strip()
    
    # 截取题目前半部分用于读白（避免太长）
    problem_for_tts = problem_clean[:200] + "..." if len(problem_clean) > 200 else problem_clean
    
    # 构建分镜脚本
    storyboard = f"""# 分镜脚本 - {title}

## 分镜设计

### 第1幕：题目朗读
**画面**: 深色背景，题目文字逐行显示
**字幕**: "{title}"
**读白**: "{problem_for_tts}"
**动画**: 
- 0.0s: 标题淡入
- 1.0s: 题目条件逐行显示
**目的**: 引入题目，让学生了解问题背景

---

### 第2幕：问题分析
**画面**: 列出已知条件和求解目标
**字幕**: "问题分析"
**读白**: "我们来分析一下这道题。首先需要明确已知条件和要求解的问题。"
**动画**:
- 0.0s: 已知条件列表显示
- 2.0s: 求解目标高亮
**目的**: 理清思路

---

### 第3幕：建立模型
**画面**: 建立数学模型或方程
**字幕**: "建立模型"
**读白**: "根据题意，我们可以建立相应的数学模型来求解。"
**动画**:
- 0.0s: 变量设定
- 1.5s: 方程或关系式显示
**目的**: 数学建模

---

### 第4幕：求解过程
**画面**: 详细求解步骤
**字幕**: "求解过程"
**读白**: "接下来我们逐步求解这个问题。"
**动画**:
- 0.0s: 第一步计算
- 2.0s: 第二步计算
- 4.0s: 得出结果
**目的**: 展示完整求解过程

---

### 第5幕：验证答案
**画面**: 验证结果的正确性
**字幕**: "验证答案"
**读白**: "让我们验证一下答案是否符合题意。"
**动画**:
- 0.0s: 代入验证
- 2.0s: 确认正确
**目的**: 确保答案正确

---

### 第6幕：总结
**画面**: 回顾解题方法和答案
**字幕**: "方法总结"
**读白**: "总结一下这道题的解题方法和关键点。"
**动画**:
- 0.0s: 答案汇总
- 2.0s: 方法要点
**目的**: 巩固知识点

---

## 音频生成清单

| 幕号 | 文件名 | 读白文本 | 时长 | 说话人 | 情感 |
|------|--------|----------|------|--------|------|
| 1 | audio_001_题目朗读.wav | "{problem_for_tts}" | | Nofish | 平和 |
| 2 | audio_002_问题分析.wav | "我们来分析一下这道题。首先需要明确已知条件和要求解的问题。" | | Nofish | 平和 |
| 3 | audio_003_建立模型.wav | "根据题意，我们可以建立相应的数学模型来求解。" | | Nofish | 平和 |
| 4 | audio_004_求解过程.wav | "接下来我们逐步求解这个问题。" | | Nofish | 平和 |
| 5 | audio_005_验证答案.wav | "让我们验证一下答案是否符合题意。" | | Nofish | 平和 |
| 6 | audio_006_总结.wav | "总结一下这道题的解题方法和关键点。" | | Nofish | 热情 |

---

## 原始题目

{problem_text}

"""
    
    if analysis_text:
        storyboard += f"""
## 数学分析

{analysis_text}
"""
    
    return storyboard


def main():
    parser = argparse.ArgumentParser(description='自动生成带题目读白的分镜脚本')
    parser.add_argument('--problem', '-p', required=True, help='完整题目文本')
    parser.add_argument('--analysis', '-a', default='', help='数学分析内容（可选）')
    parser.add_argument('--title', '-t', default='', help='视频标题（可选）')
    parser.add_argument('--output', '-o', default='storyboard.md', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 生成分镜
    storyboard = generate_storyboard(args.problem, args.analysis, args.title)
    
    # 保存文件
    output_path = Path(args.output)
    output_path.write_text(storyboard, encoding='utf-8')
    
    print(f"✅ 分镜脚本已生成: {output_path}")
    print(f"   包含6幕，第1幕为题目朗读")
    print(f"   预计TTS时长: 约60-90秒")


if __name__ == "__main__":
    main()
