"""抛物线综合题 - 完整版带MathTex公式"""
from manim import *

class ParabolaProblem(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 第1幕：标题
        title = MathTex(r"\text{抛物线综合题}", font_size=48, color="#3498db")
        subtitle = MathTex(r"y = ax^2 + bx + 4,\; B(3,0),\; \text{对称轴}x=1", 
                          font_size=28, color="#f39c12")
        VGroup(title, subtitle).arrange(DOWN, buff=0.5).center()
        
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # 第2幕：求点A
        step1 = MathTex(r"\text{步骤1: 利用对称性求点A}", font_size=36, color="#3498db")
        calc = MathTex(r"\frac{x_A + 3}{2} = 1 \Rightarrow x_A = -1", font_size=32)
        result1 = MathTex(r"A(-1, 0)", font_size=36, color="#2ecc71")
        VGroup(step1, calc, result1).arrange(DOWN, buff=0.6).center()
        
        self.play(FadeIn(step1))
        self.wait(1)
        self.play(Write(calc))
        self.wait(1)
        self.play(Write(result1))
        self.wait(3)
        self.play(FadeOut(step1), FadeOut(calc), FadeOut(result1))
        
        # 第3幕：求解析式
        step2 = MathTex(r"\text{步骤2: 待定系数法}", font_size=36, color="#3498db")
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
        self.wait(4)
        self.play(FadeOut(step2), FadeOut(eq1), FadeOut(eq2), FadeOut(sol), FadeOut(final))
        
        # 第4幕：答案
        answer = VGroup(
            MathTex(r"\text{答案:}", font_size=40, color="#3498db"),
            MathTex(r"(1)\; y = -\frac{4}{3}x^2 + \frac{8}{3}x + 4", font_size=30),
            MathTex(r"(2)\; P_1(2, 4) \text{ 或 } P_2\left(\frac{7}{3}, \frac{20}{9}\right)", font_size=28)
        ).arrange(DOWN, buff=0.5).center()
        
        box = SurroundingRectangle(answer, color="#2ecc71", buff=0.3)
        
        self.play(FadeIn(answer))
        self.play(Create(box))
        self.wait(5)
