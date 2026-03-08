"""
抛物线综合题 - 简化版（避免 LaTeX 中文问题）
"""

from manim import *
import json
from pathlib import Path


class ParabolaProblem(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        self.script_dir = Path(__file__).parent
        self.audio_dir = self._find_audio_dir()
        self.audio_timings = self.load_audio_timings()
        
        self.scene_1_title()
        self.scene_2_AB()
        self.scene_3_CD()
        self.scene_4_area()
        self.scene_5_max()
        self.scene_6_setup()
        self.scene_7_cases()
        self.scene_8_summary()
    
    def _find_audio_dir(self):
        candidates = [Path(__file__).parent / "audio"]
        for c in candidates:
            if c.exists() and any(c.glob("*.wav")):
                return c
        return Path(__file__).parent / "audio"
    
    def load_audio_timings(self):
        try:
            with open(self.audio_dir / "audio_info.json", "r") as f:
                audio_info = json.load(f)
                return {item["scene"]: item["duration"] for item in audio_info["files"]}
        except:
            return {i: 10.0 for i in range(1, 20)}
    
    def add_scene_audio(self, scene_num):
        audio_file = self.audio_dir / f"audio_{scene_num:03d}_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
    
    def wait_for_audio(self, scene_num, animation_duration=0):
        audio_duration = self.audio_timings.get(scene_num, 10.0)
        wait_time = max(0, audio_duration - animation_duration)
        if wait_time > 0:
            self.wait(wait_time)
    
    def scene_1_title(self):
        self.add_scene_audio(1)
        title = Text("抛物线综合题", font_size=48, color="#3498db")
        formula = Text("y = -x² + 2x + 3", font_size=32, color=WHITE)
        q1 = Text("(1) 求 A、B、C、D 坐标", font_size=24, color="#2ecc71")
        q2 = Text("(2) 求△PAC 面积最大时的 P 点", font_size=24, color="#2ecc71")
        q3 = Text("(3) 对称轴上是否存在点 Q 使△QBC 为等腰三角形？", font_size=24, color="#2ecc71")
        
        content = VGroup(title, formula, q1, q2, q3).arrange(DOWN, buff=0.4).center()
        start_time = self.time
        self.play(FadeIn(title), FadeIn(formula), FadeIn(q1), FadeIn(q2), FadeIn(q3))
        self.wait_for_audio(1, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_2_AB(self):
        self.add_scene_audio(2)
        title = Text("第 (1) 问：求 A、B 坐标", font_size=40, color="#3498db")
        eq1 = Text("令 y = 0：", font_size=28)
        eq2 = Text("-x² + 2x + 3 = 0", font_size=28)
        eq3 = Text("x² - 2x - 3 = 0", font_size=28)
        eq4 = Text("(x-3)(x+1) = 0", font_size=28, color="#f39c12")
        result = Text("∴ A(-1, 0), B(3, 0)", font_size=32, color="#2ecc71")
        
        content = VGroup(title, eq1, eq2, eq3, eq4, result).arrange(DOWN, buff=0.35).center()
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(eq1), Write(eq2), Write(eq3), Write(eq4), Write(result))
        self.wait_for_audio(2, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_3_CD(self):
        self.add_scene_audio(3)
        title = Text("求 C、D 坐标", font_size=40, color="#3498db")
        c1 = Text("求 C 点（与 y 轴交点）：", font_size=24, color="#f39c12")
        c2 = Text("令 x = 0，得 y = 3", font_size=24)
        c3 = Text("∴ C(0, 3)", font_size=28, color="#2ecc71")
        d1 = Text("求顶点 D：", font_size=24, color="#f39c12")
        d2 = Text("x = -b/(2a) = 1", font_size=24)
        d3 = Text("y = -1 + 2 + 3 = 4", font_size=24)
        d4 = Text("∴ D(1, 4)", font_size=28, color="#2ecc71")
        
        content = VGroup(title, c1, c2, c3, d1, d2, d3, d4).arrange(DOWN, buff=0.3).center()
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(c1), Write(c2), Write(c3))
        self.play(Write(d1), Write(d2), Write(d3), Write(d4))
        self.wait_for_audio(3, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_4_area(self):
        self.add_scene_audio(4)
        title = Text("第 (2) 问：求△PAC 面积最大值", font_size=36, color="#3498db")
        p1 = Text("设 P(x, -x²+2x+3)，0 < x < 3", font_size=24)
        p2 = Text("S△PAC = ½ |xA(yC-yP) + xC(yP-yA) + xP(yA-yC)|", font_size=20)
        p3 = Text("= ½ |-1(3-yP) + 0 + x(0-3)|", font_size=20)
        p4 = Text("= ½ |-3 + yP - 3x|", font_size=24, color="#f39c12")
        
        content = VGroup(title, p1, p2, p3, p4).arrange(DOWN, buff=0.35).center()
        start_time = self.time
        self.play(FadeIn(title), FadeIn(p1))
        self.play(Write(p2), Write(p3), Write(p4))
        self.wait_for_audio(4, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_5_max(self):
        self.add_scene_audio(5)
        title = Text("求面积最大值", font_size=40, color="#3498db")
        m1 = Text("S = ½ |-3 + (-x²+2x+3) - 3x| = ½ |-x² - x|", font_size=22)
        m2 = Text("= ½ (x² + x)  (∵ x > 0)", font_size=24, color="#f39c12")
        m3 = Text("求导：S' = ½ (2x + 1)", font_size=24)
        m4 = Text("令 S' = 0：x = -½ (舍去)", font_size=22, color="#e74c3c")
        m5 = Text("∴ 在 (0,3) 内，S 单调递增", font_size=22)
        m6 = Text("当 x = 3 时，Smax = 6，此时 P(3, 0)", font_size=28, color="#2ecc71")
        
        content = VGroup(title, m1, m2, m3, m4, m5, m6).arrange(DOWN, buff=0.3).center()
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(m1), Write(m2))
        self.play(Write(m3), Write(m4), Write(m5), Write(m6))
        self.wait_for_audio(5, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_6_setup(self):
        self.add_scene_audio(6)
        title = Text("第 (3) 问：等腰三角形存在性", font_size=36, color="#3498db")
        s1 = Text("对称轴：x = 1", font_size=28)
        s2 = Text("设 Q(1, y)", font_size=28)
        s3 = Text("B(3, 0), C(0, 3)", font_size=28, color="#f39c12")
        s4 = Text("QB² = (3-1)² + (0-y)² = 4 + y²", font_size=22)
        s5 = Text("QC² = (0-1)² + (3-y)² = 1 + (3-y)²", font_size=22)
        s6 = Text("BC² = (3-0)² + (0-3)² = 18", font_size=22)
        
        content = VGroup(title, s1, s2, s3, s4, s5, s6).arrange(DOWN, buff=0.3).center()
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(s1), Write(s2), Write(s3))
        self.play(Write(s4), Write(s5), Write(s6))
        self.wait_for_audio(6, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_7_cases(self):
        self.add_scene_audio(7)
        title = Text("三种情况讨论", font_size=40, color="#3498db")
        c1 = Text("情况 1：QB = QC", font_size=24, color="#f39c12")
        c1_eq = Text("4 + y² = 1 + (3-y)²", font_size=22)
        c1_sol = Text("解得：y = 1  ∴ Q₁(1, 1)", font_size=22, color="#2ecc71")
        c2 = Text("情况 2：QB = BC", font_size=24, color="#f39c12")
        c2_eq = Text("4 + y² = 18", font_size=22)
        c2_sol = Text("解得：y = ±√14  ∴ Q₂,₃(1, ±√14)", font_size=22, color="#2ecc71")
        c3 = Text("情况 3：QC = BC", font_size=24, color="#f39c12")
        c3_eq = Text("1 + (3-y)² = 18", font_size=22)
        c3_sol = Text("解得：y = 3±√17  ∴ Q₄,₅(1, 3±√17)", font_size=22, color="#2ecc71")
        
        content = VGroup(
            title,
            VGroup(c1, c1_eq, c1_sol).arrange(DOWN, buff=0.3),
            VGroup(c2, c2_eq, c2_sol).arrange(DOWN, buff=0.3),
            VGroup(c3, c3_eq, c3_sol).arrange(DOWN, buff=0.3)
        ).arrange(DOWN, buff=0.4).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(c1), Write(c1_eq), Write(c1_sol))
        self.play(Write(c2), Write(c2_eq), Write(c2_sol))
        self.play(Write(c3), Write(c3_eq), Write(c3_sol))
        self.wait_for_audio(7, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_8_summary(self):
        self.add_scene_audio(8)
        title = Text("答案汇总", font_size=44, color="#3498db")
        a1 = Text("(1) A(-1,0), B(3,0), C(0,3), D(1,4)", font_size=24)
        a2 = Text("(2) P(3,0), Smax = 6", font_size=24, color="#2ecc71")
        a3 = Text("(3) 存在 5 个点 Q：", font_size=22)
        a3_detail = Text("(1,1), (1,±√14), (1,3±√17)", font_size=20, color="#2ecc71")
        thanks = Text("谢谢观看！", font_size=48, color="#3498db")
        
        content = VGroup(title, a1, a2, a3, a3_detail, thanks).arrange(DOWN, buff=0.5).center()
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(a1), Write(a2))
        self.play(Write(a3), Write(a3_detail))
        self.play(Write(thanks))
        self.wait_for_audio(8, self.time - start_time)
        self.play(FadeOut(content))
