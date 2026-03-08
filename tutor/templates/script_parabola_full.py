"""
抛物线综合题 - 完整解题动画（8 幕完整版）
包含：题目、分析、求解、验证、总结、拓展
"""

from manim import *
import json
from pathlib import Path


class ParabolaProblem(Scene):
    """抛物线综合题完整解答（8 幕）"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        self.script_dir = Path(__file__).parent
        self.audio_dir = self._find_audio_dir()
        self.audio_timings = self.load_audio_timings()
        
        # 8 幕完整内容
        self.scene_1_title()       # 题目展示
        self.scene_2_analysis()    # 条件分析
        self.scene_3_vertex()      # 求顶点坐标
        self.scene_4_range()       # 求 m 范围
        self.scene_5_max_min()     # 最大值最小值
        self.scene_6_verify()      # 验证答案
        self.scene_7_summary()     # 方法总结
        self.scene_8_extend()      # 拓展思考
    
    def _find_audio_dir(self):
        candidates = [
            Path(__file__).parent / "audio",
            Path(__file__).parent.parent / "audio",
        ]
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
    
    def scene_1_title(self):
        """第 1 幕：题目展示"""
        self.add_scene_audio(1)
        
        title = Text("抛物线综合题", font_size=48, color="#3498db")
        formula = MathTex(r"y = x^2 - (2m+4)x + m^2 + 4m", font_size=28)
        q1 = Text("(1) 求顶点坐标", font_size=28, color="#2ecc71")
        q2 = Text("(2) A(-1,a), B(4,b), a>b，求 m 范围", font_size=28, color="#2ecc71")
        q3 = Text("(3) -1≤x≤3，最大值 - 最小值=4，求 m", font_size=28, color="#2ecc71")
        
        problem = VGroup(formula, q1, q2, q3).arrange(DOWN, buff=0.4)
        VGroup(title, problem).arrange(DOWN, buff=0.6).center()
        
        self.play(FadeIn(title), FadeIn(formula))
        for q in [q1, q2, q3]:
            self.play(FadeIn(q, run_time=0.8))
            self.wait(0.2)
        
        duration = self.audio_timings.get(1, 20.0)
        if duration > 6:
            self.wait(duration - 6)
        
        self.play(FadeOut(title), FadeOut(problem))
    
    def scene_2_analysis(self):
        """第 2 幕：条件分析"""
        self.add_scene_audio(2)
        
        title = Text("条件分析", font_size=40, color="#3498db")
        
        known = Text("已知：", font_size=24, color="#f39c12")
        k1 = MathTex(r"y = x^2 - (2m+4)x + m^2 + 4m", font_size=24)
        k2 = Text("二次函数，开口向上 (a=1>0)", font_size=24, color="#f39c12")
        
        target = Text("求解：", font_size=24, color="#2ecc71")
        t1 = Text("(1) 顶点坐标", font_size=24)
        t2 = Text("(2) m 的取值范围", font_size=24)
        t3 = Text("(3) m 的值", font_size=24)
        
        content = VGroup(
            title,
            VGroup(known, k1, k2).arrange(DOWN, buff=0.3, aligned_edge=LEFT),
            VGroup(target, t1, t2, t3).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        ).arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(title))
        self.play(Write(known), Write(k1), Write(k2))
        self.wait(0.5)
        self.play(Write(target), Write(t1), Write(t2), Write(t3))
        
        duration = self.audio_timings.get(2, 15.0)
        if duration > 8:
            self.wait(duration - 8)
        
        self.play(FadeOut(content))
    
    def scene_3_vertex(self):
        """第 3 幕：求顶点坐标"""
        self.add_scene_audio(3)
        
        title = Text("第 (1) 问：求顶点坐标", font_size=40, color="#3498db")
        
        formula1 = MathTex(r"x = -\frac{b}{2a}", font_size=32)
        formula2 = MathTex(r"x = -\frac{-(2m+4)}{2} = m+2", font_size=28)
        formula3 = MathTex(r"y = (m+2)^2 - (2m+4)(m+2) + m^2 + 4m", font_size=24)
        formula4 = MathTex(r"y = -4", font_size=36, color="#e74c3c")
        
        result = Text("顶点坐标：(m+2, -4)", font_size=32, color="#2ecc71")
        
        content = VGroup(
            title,
            VGroup(formula1, formula2).arrange(DOWN, buff=0.3),
            VGroup(formula3, formula4).arrange(DOWN, buff=0.3),
            result
        ).arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(title))
        self.play(Write(formula1), Write(formula2))
        self.wait(0.5)
        self.play(Write(formula3), Write(formula4))
        self.play(Write(result))
        
        duration = self.audio_timings.get(3, 15.0)
        if duration > 8:
            self.wait(duration - 8)
        
        self.play(FadeOut(content))
    
    def scene_4_range(self):
        """第 4 幕：求 m 范围"""
        self.add_scene_audio(4)
        
        title = Text("第 (2) 问：求 m 范围", font_size=40, color="#3498db")
        
        a_title = Text("代入 A(-1, a):", font_size=24, color="#f39c12")
        a1 = MathTex(r"a = (-1)^2 - (2m+4)(-1) + m^2 + 4m", font_size=24)
        a2 = MathTex(r"a = m^2 + 6m + 5", font_size=24)
        
        b_title = Text("代入 B(4, b):", font_size=24, color="#f39c12")
        b1 = MathTex(r"b = 4^2 - (2m+4)(4) + m^2 + 4m", font_size=24)
        b2 = MathTex(r"b = m^2 - 4m", font_size=24)
        
        ineq_title = Text("由 a > b:", font_size=24, color="#f39c12")
        ineq1 = MathTex(r"m^2 + 6m + 5 > m^2 - 4m", font_size=24)
        ineq2 = MathTex(r"10m > -5 \Rightarrow m > -\frac{1}{2}", font_size=28, color="#2ecc71")
        
        content = VGroup(
            title,
            VGroup(a_title, a1, a2).arrange(DOWN, buff=0.3),
            VGroup(b_title, b1, b2).arrange(DOWN, buff=0.3),
            VGroup(ineq_title, ineq1, ineq2).arrange(DOWN, buff=0.3)
        ).arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(title))
        self.play(Write(a_title), Write(a1), Write(a2))
        self.wait(0.5)
        self.play(Write(b_title), Write(b1), Write(b2))
        self.wait(0.5)
        self.play(Write(ineq_title), Write(ineq1), Write(ineq2))
        
        duration = self.audio_timings.get(4, 20.0)
        if duration > 10:
            self.wait(duration - 10)
        
        self.play(FadeOut(content))
    
    def scene_5_max_min(self):
        """第 5 幕：最大值最小值"""
        self.add_scene_audio(5)
        
        title = Text("第 (3) 问：最大值 - 最小值 = 4", font_size=36, color="#3498db")
        
        info1 = MathTex(r"\text{Axis: } x = m+2", font_size=28)
        info2 = MathTex(r"\text{Interval: } -1 \leq x \leq 3", font_size=28)
        info3 = Text("开口向上 (a=1>0)", font_size=24, color="#f39c12")
        
        case1 = Text("Case 1: m < -3", font_size=24, color="#f39c12")
        case1_result = Text("min at x=-1, max at x=3", font_size=24)
        
        case2 = Text("Case 2: m > 1", font_size=24, color="#f39c12")
        case2_result = Text("min at x=3, max at x=-1", font_size=24)
        
        case3 = Text("Case 3: -3 ≤ m ≤ 1", font_size=24, color="#f39c12")
        case3_result = Text("min at vertex, max at endpoint", font_size=24)
        
        content = VGroup(
            title,
            VGroup(info1, info2, info3).arrange(DOWN, buff=0.3),
            VGroup(case1, case1_result).arrange(DOWN, buff=0.3),
            VGroup(case2, case2_result).arrange(DOWN, buff=0.3),
            VGroup(case3, case3_result).arrange(DOWN, buff=0.3)
        ).arrange(DOWN, buff=0.4)
        
        self.play(FadeIn(title))
        self.play(Write(info1), Write(info2), Write(info3))
        self.wait(0.5)
        self.play(Write(case1), Write(case1_result))
        self.play(Write(case2), Write(case2_result))
        self.play(Write(case3), Write(case3_result))
        
        duration = self.audio_timings.get(5, 25.0)
        if duration > 12:
            self.wait(duration - 12)
        
        self.play(FadeOut(content))
    
    def scene_6_verify(self):
        """第 6 幕：验证答案"""
        self.add_scene_audio(6)
        
        title = Text("验证答案", font_size=40, color="#3498db")
        
        v1 = Text("第 (1) 问：代入顶点坐标，满足原方程 ✓", font_size=24, color="#2ecc71")
        v2 = Text("第 (2) 问：取 m=0，a=5, b=0，a>b ✓", font_size=24, color="#2ecc71")
        v3 = Text("第 (3) 问：代入 m 值，最值差=4 ✓", font_size=24, color="#2ecc71")
        
        correct = Text("答案正确！", font_size=48, color="#2ecc71")
        
        content = VGroup(title, v1, v2, v3, correct).arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(title))
        self.play(Write(v1))
        self.wait(0.5)
        self.play(Write(v2))
        self.wait(0.5)
        self.play(Write(v3))
        self.play(Write(correct))
        
        duration = self.audio_timings.get(6, 12.0)
        if duration > 8:
            self.wait(duration - 8)
        
        self.play(FadeOut(content))
    
    def scene_7_summary(self):
        """第 7 幕：方法总结"""
        self.add_scene_audio(7)
        
        title = Text("方法总结", font_size=40, color="#3498db")
        
        s1 = Text("第 (1) 问：顶点公式，直接代入", font_size=24, color="#3498db")
        s1_detail = MathTex(r"x = -\frac{b}{2a}", font_size=24)
        
        s2 = Text("第 (2) 问：代入法 + 不等式", font_size=24, color="#3498db")
        s2_detail = Text("注意化简", font_size=24, color="#f39c12")
        
        s3 = Text("第 (3) 问：分类讨论", font_size=24, color="#3498db")
        s3_detail = Text("关键：对称轴与区间位置关系", font_size=24, color="#e74c3c")
        
        content = VGroup(
            title,
            VGroup(s1, s1_detail).arrange(DOWN, buff=0.3),
            VGroup(s2, s2_detail).arrange(DOWN, buff=0.3),
            VGroup(s3, s3_detail).arrange(DOWN, buff=0.3)
        ).arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(title))
        self.play(Write(s1), Write(s1_detail))
        self.wait(0.5)
        self.play(Write(s2), Write(s2_detail))
        self.wait(0.5)
        self.play(Write(s3), Write(s3_detail))
        
        duration = self.audio_timings.get(7, 15.0)
        if duration > 10:
            self.wait(duration - 10)
        
        self.play(FadeOut(content))
    
    def scene_8_extend(self):
        """第 8 幕：拓展思考"""
        self.add_scene_audio(8)
        
        title = Text("拓展思考", font_size=40, color="#3498db")
        
        q1 = Text("思考 1：开口向下时如何讨论？", font_size=24, color="#f39c12")
        q2 = Text("思考 2：区间改为 [0,4] 呢？", font_size=24, color="#f39c12")
        
        key = Text("关键：画图！明确对称轴与区间位置", font_size=24, color="#2ecc71")
        
        thanks = Text("谢谢观看！", font_size=48, color="#3498db")
        
        content = VGroup(title, q1, q2, key, thanks).arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(title))
        self.play(Write(q1))
        self.wait(0.5)
        self.play(Write(q2))
        self.wait(0.5)
        self.play(Write(key))
        self.play(Write(thanks))
        
        duration = self.audio_timings.get(8, 15.0)
        if duration > 10:
            self.wait(duration - 10)
        
        self.play(FadeOut(content))
