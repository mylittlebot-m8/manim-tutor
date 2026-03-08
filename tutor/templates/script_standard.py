"""
标准教学视频脚本模板 - 支持 LaTeX 中文

核心配置：
1. 使用 xelatex 编译器（支持中文）
2. 配置 xeCJK 包和中文字体
3. MathTex 只显示纯公式（无中文）
4. Text 显示中文说明
5. 两者配合使用
"""

from manim import *
import json
from pathlib import Path

# ========== 关键配置：使用 xelatex 支持中文 ==========
config.tex_compiler = "xelatex"

# 创建支持中文的 TexTemplate
template = TexTemplate()
template.tex_compiler = "xelatex"
template.output_format = ".xdv"  # xelatex 输出 .xdv 格式
template.add_to_preamble(r"\usepackage{xeCJK}")
template.add_to_preamble(r"\setCJKmainfont{WenQuanYi Zen Hei}")
# ==================================================


class StandardTeachingScene(Scene):
    """标准教学场景基类"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        self.script_dir = Path(__file__).parent
        self.audio_dir = self._find_audio_dir()
        self.audio_timings = self.load_audio_timings()
        
        # 子类实现具体的 scene_1, scene_2 等方法
        # self.scene_1_title()
        # self.scene_2_analysis()
        # ...
    
    def _find_audio_dir(self):
        """智能查找音频目录"""
        candidates = [
            Path(__file__).parent / "audio",
            Path(__file__).parent.parent / "audio",
        ]
        for c in candidates:
            if c.exists() and any(c.glob("*.wav")):
                return c
        return Path(__file__).parent / "audio"
    
    def load_audio_timings(self):
        """加载音频时长信息"""
        try:
            with open(self.audio_dir / "audio_info.json", "r") as f:
                audio_info = json.load(f)
                return {item["scene"]: item["duration"] for item in audio_info["files"]}
        except:
            return {i: 10.0 for i in range(1, 20)}
    
    def add_scene_audio(self, scene_num):
        """添加场景音频"""
        audio_file = self.audio_dir / f"audio_{scene_num:03d}_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
    
    def wait_for_audio(self, scene_num, animation_duration=0):
        """等待到音频结束"""
        audio_duration = self.audio_timings.get(scene_num, 10.0)
        wait_time = max(0, audio_duration - animation_duration)
        if wait_time > 0:
            self.wait(wait_time)
    
    # ========== 标准组件方法 ==========
    
    def create_title(self, text: str, font_size: int = 48, color: str = "#3498db"):
        """创建标题（纯中文用 Text）"""
        return Text(text, font_size=font_size, color=color)
    
    def create_formula(self, latex: str, font_size: int = 28, color: str = WHITE):
        """
        创建公式（使用支持中文的模板）
        
        Args:
            latex: LaTeX 公式内容
            font_size: 字体大小
            color: 颜色
        
        Returns:
            Tex 或 MathTex 对象
        """
        # 如果包含中文，使用 Tex
        if any('\u4e00' <= c <= '\u9fff' for c in latex):
            return Tex(latex, font_size=font_size, color=color, tex_template=template)
        else:
            return MathTex(latex, font_size=font_size, color=color, tex_template=template)
    
    def create_step(self, step_text: str, formula_latex: str = None, 
                    detail_text: str = None, highlight: bool = False):
        """
        创建详细步骤（面向学生）
        
        Args:
            step_text: 步骤标题（如"步骤 1：令 y = 0"）
            formula_latex: LaTeX 公式（可选）
            detail_text: 详细说明（如"因为与 x 轴交点，所以 y 坐标为 0"）
            highlight: 是否高亮（重点步骤）
        
        Returns:
            VGroup: 组合对象
        """
        color = "#f39c12" if highlight else "#3498db"
        elements = []
        
        # 步骤标题
        step_title = Text(step_text, font_size=28, color=color)
        elements.append(step_title)
        
        # 公式（如果有）
        if formula_latex:
            formula = self.create_formula(formula_latex, font_size=26)
            elements.append(formula)
        
        # 详细说明（如果有）
        if detail_text:
            detail = Text(detail_text, font_size=22, color="#7f8c8d")
            elements.append(detail)
        
        return VGroup(*elements).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    
    def create_result(self, text: str, color: str = "#2ecc71", font_size: int = 28):
        """创建结果展示（支持 ∴ 符号）"""
        if text.startswith("∴"):
            # 分离 ∴ 符号和后续内容
            parts = text.split("∴", 1)
            if len(parts) == 2:
                symbol = Text("∴", font_size=font_size, color=color)
                content = Text(parts[1].strip(), font_size=font_size, color=color)
                return VGroup(symbol, content).arrange(RIGHT, buff=0.2)
        return Text(text, font_size=font_size, color=color)
    
    # ========== 标准场景模板 ==========
    
    def standard_scene_with_steps(self, scene_num: int, title: str, steps: list):
        """
        标准步骤场景
        
        Args:
            scene_num: 场景编号
            title: 场景标题
            steps: 步骤列表，每项为 (中文说明，LaTeX 公式或 None)
        
        示例:
            steps = [
                ("令 y = 0：", "-x^2 + 2x + 3 = 0"),
                ("整理得：", "x^2 - 2x - 3 = 0"),
                ("因式分解：", "(x-3)(x+1) = 0"),
            ]
        """
        self.add_scene_audio(scene_num)
        
        # 标题
        title_mobject = self.create_title(title)
        
        # 步骤
        step_mobjects = []
        for step_text, formula in steps:
            step_mobjects.append(self.create_step(step_text, formula))
        
        steps_group = VGroup(*step_mobjects).arrange(DOWN, buff=0.35)
        
        # 组合
        content = VGroup(title_mobject, steps_group).arrange(DOWN, buff=0.5).center()
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title_mobject))
        for step in step_mobjects:
            self.play(Write(step))
        self.wait_for_audio(scene_num, self.time - start_time)
        
        self.play(FadeOut(content))


# ========== 使用示例 ==========
"""
class MyParabolaProblem(StandardTeachingScene):
    def construct(self):
        super().construct()
        self.scene_1_find_AB()
    
    def scene_1_find_AB(self):
        '''第 1 问：求 A、B 坐标'''
        steps = [
            ("令 y = 0：", "-x^2 + 2x + 3 = 0"),
            ("整理得：", "x^2 - 2x - 3 = 0"),
            ("因式分解：", "(x-3)(x+1) = 0"),
            (None, "\\therefore x_1 = -1, x_2 = 3"),
            ("∴ A(-1, 0), B(3, 0)", None),
        ]
        self.standard_scene_with_steps(1, "求 A、B 坐标", steps)
"""
