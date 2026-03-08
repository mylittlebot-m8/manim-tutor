"""抛物线综合题 - 带TTS音频版本"""
from manim import *
import json
from pathlib import Path

class ParabolaProblem(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 加载音频时长
        self.script_dir = Path(__file__).parent
        self.audio_timings = self.load_audio_timings()
        
        # 执行各幕
        self.scene_1_title()
        self.scene_2_find_a()
        self.scene_3_equation()
        self.scene_4_answer()
    
    def load_audio_timings(self):
        """加载音频时长信息"""
        try:
            audio_info_path = self.script_dir / "audio" / "audio_info.json"
            with open(audio_info_path, "r") as f:
                audio_info = json.load(f)
                return {item["scene"]: item["duration"] for item in audio_info["files"]}
        except:
            return {i: 10.0 for i in range(1, 20)}
    
    def add_scene_audio(self, scene_num):
        """添加场景音频"""
        audio_file = self.script_dir / "audio" / f"audio_{scene_num:03d}_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
    
    def scene_1_title(self):
        """第1幕：标题"""
        self.add_scene_audio(1)
        
        title = Text("抛物线综合题", font_size=48, color="#3498db")
        subtitle = MathTex(r"y = ax^2 + bx + 4,\; B(3,0),\; x=1", 
                          font_size=28, color="#f39c12")
        VGroup(title, subtitle).arrange(DOWN, buff=0.5).center()
        
        self.play(FadeIn(title), FadeIn(subtitle))
        
        duration = self.audio_timings.get(1, 10.0)
        self.wait(duration)
        
        self.play(FadeOut(title), FadeOut(subtitle))
    
    def scene_2_find_a(self):
        """第2幕：求点A"""
        self.add_scene_audio(2)
        
        step1 = Text("步骤1: 利用对称性求点A", font_size=36, color="#3498db")
        calc = MathTex(r"\frac{x_A + 3}{2} = 1 \Rightarrow x_A = -1", font_size=32)
        result1 = MathTex(r"A(-1, 0)", font_size=36, color="#2ecc71")
        VGroup(step1, calc, result1).arrange(DOWN, buff=0.6).center()
        
        self.play(FadeIn(step1))
        self.wait(0.5)
        self.play(Write(calc))
        self.wait(0.5)
        self.play(Write(result1))
        
        duration = self.audio_timings.get(2, 10.0)
        elapsed = 2.0
        if duration > elapsed:
            self.wait(duration - elapsed)
        
        self.play(FadeOut(step1), FadeOut(calc), FadeOut(result1))
    
    def scene_3_equation(self):
        """第3幕：求解析式"""
        self.add_scene_audio(3)
        
        step2 = Text("步骤2: 待定系数法", font_size=36, color="#3498db")
        eq1 = MathTex(r"a - b = -4", font_size=28)
        eq2 = MathTex(r"-\frac{b}{2a} = 1 \Rightarrow b = -2a", font_size=28)
        sol = MathTex(r"a = -\frac{4}{3},\; b = \frac{8}{3}", font_size=28, color="#2ecc71")
        final = MathTex(r"y = -\frac{4}{3}x^2 + \frac{8}{3}x + 4", font_size=32, color="#e74c3c")
        VGroup(step2, eq1, eq2, sol, final).arrange(DOWN, buff=0.4).center()
        
        self.play(FadeIn(step2))
        self.play(Write(eq1))
        self.play(Write(eq2))
        self.play(Write(sol))
        self.play(Write(final))
        
        duration = self.audio_timings.get(3, 15.0)
        elapsed = 5.0
        if duration > elapsed:
            self.wait(duration - elapsed)
        
        self.play(FadeOut(step2), FadeOut(eq1), FadeOut(eq2), FadeOut(sol), FadeOut(final))
    
    def scene_4_answer(self):
        """第4幕：答案"""
        self.add_scene_audio(4)
        
        answer_title = Text("答案:", font_size=40, color="#3498db")
        ans1 = MathTex(r"(1)\; y = -\frac{4}{3}x^2 + \frac{8}{3}x + 4", font_size=30)
        
        ans2_label = Text("(2)", font_size=30)
        ans2_p1 = MathTex(r"P_1(2, 4)", font_size=28)
        ans2_or = Text("or", font_size=28, color="yellow")
        ans2_p2 = MathTex(r"P_2(\frac{7}{3}, \frac{20}{9})", font_size=28)
        
        ans2_row = VGroup(ans2_label, ans2_p1, ans2_or, ans2_p2).arrange(RIGHT, buff=0.3)
        
        answer = VGroup(answer_title, ans1, ans2_row).arrange(DOWN, buff=0.5).center()
        
        box = SurroundingRectangle(answer, color="#2ecc71", buff=0.3)
        
        self.play(FadeIn(answer_title))
        self.play(Write(ans1))
        self.play(FadeIn(ans2_row))
        self.play(Create(box))
        
        duration = self.audio_timings.get(4, 10.0)
        elapsed = 3.0
        if duration > elapsed:
            self.wait(duration - elapsed)
