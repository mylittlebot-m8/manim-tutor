"""
抛物线综合题 - 中文版（支持中文MathTex）
"""
from manim import *
import json
from pathlib import Path

class ParabolaProblem(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        self.script_dir = Path(__file__).parent
        self.audio_timings = self.load_audio_timings()
        
        self.scene_1_title()
        self.scene_2_find_a()
        self.scene_3_equation()
        self.scene_4_answer()
    
    def load_audio_timings(self):
        try:
            audio_info_path = self.script_dir / "audio" / "audio_info.json"
            with open(audio_info_path, "r") as f:
                audio_info = json.load(f)
                return {item["scene"]: item["duration"] for item in audio_info["files"]}
        except:
            return {i: 10.0 for i in range(1, 20)}
    
    def add_scene_audio(self, scene_num):
        audio_file = self.script_dir / "audio" / f"audio_{scene_num:03d}_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
    
    def scene_1_title(self):
        """第1幕：题目展示"""
        self.add_scene_audio(1)
        
        title = Text("抛物线综合题", font_size=48, color="#3498db")
        
        # 使用MathTex显示公式和中文
        problem = VGroup(
            MathTex(r"y = ax^2 + bx + 4", font_size=32),
            MathTex(r"B(3, 0),\; \text{对称轴}\; x = 1", font_size=28, color="#f39c12"),
            MathTex(r"(1)\; \text{求解析式}", font_size=26, color="#2ecc71"),
            MathTex(r"(2)\; \angle PCB = \angle ABC,\; \text{求点}P", font_size=26, color="#2ecc71")
        ).arrange(DOWN, buff=0.4)
        
        VGroup(title, problem).arrange(DOWN, buff=0.6).center()
        
        self.play(FadeIn(title))
        self.wait(0.5)
        
        for line in problem:
            self.play(FadeIn(line, run_time=0.8))
            self.wait(0.2)
        
        duration = self.audio_timings.get(1, 15.0)
        elapsed = len(problem) * 1.0 + 1.0
        if duration > elapsed:
            self.wait(duration - elapsed)
        
        self.play(FadeOut(title), FadeOut(problem))
    
    def scene_2_find_a(self):
        """第2幕：利用对称性求点A"""
        self.add_scene_audio(2)
        
        step1 = Text("步骤1: 利用对称性求点A", font_size=36, color="#3498db")
        
        calc = MathTex(r"\frac{x_A + 3}{2} = 1", font_size=32)
        arrow = MathTex(r"\Rightarrow", font_size=36, color="#f39c12")
        result = MathTex(r"x_A = -1", font_size=36, color="#2ecc71")
        final = MathTex(r"A(-1, 0)", font_size=40, color="#e74c3c")
        
        row = VGroup(calc, arrow, result).arrange(RIGHT, buff=0.5)
        content = VGroup(step1, row, final).arrange(DOWN, buff=0.8).center()
        
        self.play(FadeIn(step1))
        self.wait(0.5)
        self.play(Write(calc))
        self.wait(0.3)
        self.play(FadeIn(arrow))
        self.wait(0.3)
        self.play(Write(result))
        self.wait(0.5)
        self.play(Write(final))
        
        duration = self.audio_timings.get(2, 12.0)
        elapsed = 4.0
        if duration > elapsed:
            self.wait(duration - elapsed)
        
        self.play(FadeOut(content))
    
    def scene_3_equation(self):
        """第3幕：待定系数法求解析式"""
        self.add_scene_audio(3)
        
        step2 = Text("步骤2: 待定系数法", font_size=36, color="#3498db")
        
        eq1 = MathTex(r"\text{代入}\; A(-1, 0):", font_size=24)
        eq1b = MathTex(r"a - b = -4 \quad ...(1)", font_size=28)
        
        eq2 = MathTex(r"\text{对称轴}:", font_size=24)
        eq2b = MathTex(r"-\frac{b}{2a} = 1 \Rightarrow b = -2a \quad ...(2)", font_size=28)
        
        sol = MathTex(r"\text{解得}:", font_size=24)
        solb = MathTex(r"a = -\frac{4}{3},\; b = \frac{8}{3}", font_size=28, color="#2ecc71")
        
        final = MathTex(r"y = -\frac{4}{3}x^2 + \frac{8}{3}x + 4", font_size=30, color="#e74c3c")
        
        content = VGroup(
            step2, 
            VGroup(eq1, eq1b).arrange(DOWN, buff=0.2),
            VGroup(eq2, eq2b).arrange(DOWN, buff=0.2),
            VGroup(sol, solb).arrange(DOWN, buff=0.2),
            final
        ).arrange(DOWN, buff=0.4).center()
        
        self.play(FadeIn(step2))
        self.wait(0.3)
        
        self.play(Write(eq1))
        self.play(Write(eq1b))
        self.wait(0.5)
        
        self.play(Write(eq2))
        self.play(Write(eq2b))
        self.wait(0.5)
        
        self.play(Write(sol))
        self.play(Write(solb))
        self.wait(0.5)
        
        self.play(Write(final))
        
        box = SurroundingRectangle(final, color="#e74c3c", buff=0.2)
        self.play(Create(box))
        
        duration = self.audio_timings.get(3, 18.0)
        elapsed = 6.0
        if duration > elapsed:
            self.wait(duration - elapsed)
        
        self.play(FadeOut(content), FadeOut(box))
    
    def scene_4_answer(self):
        """第4幕：最终答案"""
        self.add_scene_audio(4)
        
        title = Text("答案", font_size=44, color="#3498db")
        
        ans1_label = MathTex(r"(1)", font_size=30)
        ans1_form = MathTex(r"y = -\frac{4}{3}x^2 + \frac{8}{3}x + 4", font_size=28)
        ans1 = VGroup(ans1_label, ans1_form).arrange(RIGHT, buff=0.5)
        
        ans2_label = MathTex(r"(2)", font_size=30)
        ans2_p1 = MathTex(r"P_1(2, 4)", font_size=26)
        ans2_or = MathTex(r"\text{或}", font_size=26, color="yellow")
        ans2_p2 = MathTex(r"P_2\left(\frac{7}{3}, \frac{20}{9}\right)", font_size=26)
        ans2_row = VGroup(ans2_p1, ans2_or, ans2_p2).arrange(RIGHT, buff=0.3)
        ans2 = VGroup(ans2_label, ans2_row).arrange(RIGHT, buff=0.5)
        
        answer = VGroup(title, ans1, ans2).arrange(DOWN, buff=0.6).center()
        
        box = SurroundingRectangle(answer, color="#2ecc71", buff=0.4)
        
        self.play(FadeIn(title))
        self.wait(0.3)
        self.play(Write(ans1))
        self.wait(0.3)
        self.play(FadeIn(ans2))
        self.play(Create(box))
        
        duration = self.audio_timings.get(4, 12.0)
        elapsed = 3.0
        if duration > elapsed:
            self.wait(duration - elapsed)
