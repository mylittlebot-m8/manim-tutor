"""
抛物线问题讲解 - Manim动画
"""

from manim import *
import numpy as np

class ParabolaScene(Scene):
    """抛物线教学场景"""
    
    def construct(self):
        # 设置背景
        self.camera.background_color = "#1a1a2e"
        
        # 创建坐标系
        axes = Axes(
            x_range=[-3, 5, 1],
            y_range=[-1, 6, 1],
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": [-2, 0, 2, 4]},
            y_axis_config={"numbers_to_include": [0, 2, 4]},
        )
        
        # 第1幕：开场标题
        title = Text("抛物线问题详解", font_size=48, color="#3498db")
        subtitle = Text("对称性与动点问题", font_size=24, color="#7f8c8d")
        subtitle.next_to(title, DOWN)
        
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # 第2幕：显示坐标系和已知条件
        self.play(Create(axes))
        self.wait(1)
        
        # 标记点B
        B = Dot(axes.c2p(3, 0), color=RED)
        B_label = Text("B(3,0)", font_size=20, color=RED).next_to(B, DOWN+RIGHT)
        
        # 对称轴
        symmetry_line = DashedLine(
            axes.c2p(1, -1),
            axes.c2p(1, 6),
            color=YELLOW,
            dash_length=0.1
        )
        symmetry_label = Text("x=1", font_size=16, color=YELLOW).next_to(symmetry_line, UP)
        
        self.play(Create(B), Write(B_label))
        self.wait(1)
        self.play(Create(symmetry_line), Write(symmetry_label))
        self.wait(2)
        
        # 第3幕：求点A
        A = Dot(axes.c2p(-1, 0), color=RED)
        A_label = Text("A(-1,0)", font_size=20, color=RED).next_to(A, DOWN+LEFT)
        
        # 画对称箭头
        arrow1 = Arrow(B.get_center(), axes.c2p(1, 0), buff=0.1, color=GREEN)
        arrow2 = Arrow(axes.c2p(1, 0), A.get_center(), buff=0.1, color=GREEN)
        
        self.play(Create(A), Write(A_label))
        self.wait(1)
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(2)
        
        # 第4幕：绘制抛物线
        parabola = axes.plot(
            lambda x: -4/3 * x**2 + 8/3 * x + 4,
            x_range=[-1.5, 3.5],
            color="#3498db",
            stroke_width=3
        )
        
        self.play(Create(parabola), run_time=2)
        self.wait(1)
        
        # 标记点C
        C = Dot(axes.c2p(0, 4), color=GREEN)
        C_label = Text("C(0,4)", font_size=20, color=GREEN).next_to(C, UP+LEFT)
        
        self.play(Create(C), Write(C_label))
        self.wait(2)
        
        # 第5幕：连线BC
        line_BC = Line(B.get_center(), C.get_center(), color=PURPLE, stroke_width=2)
        self.play(Create(line_BC))
        self.wait(2)
        
        # 第6幕：标记答案点P1和P2
        P1 = Dot(axes.c2p(2, 4), color=ORANGE)
        P1_label = Text("P₁(2,4)", font_size=18, color=ORANGE).next_to(P1, UP+RIGHT)
        
        P2 = Dot(axes.c2p(7/3, 20/9), color=ORANGE)
        P2_label = Text("P₂(7/3, 20/9)", font_size=16, color=ORANGE).next_to(P2, DOWN+RIGHT)
        
        self.play(Create(P1), Write(P1_label))
        self.wait(1)
        self.play(Create(P2), Write(P2_label))
        self.wait(2)
        
        # 连线P1C和P2C
        line_P1C = Line(P1.get_center(), C.get_center(), color=ORANGE, stroke_width=2)
        line_P2C = Line(P2.get_center(), C.get_center(), color=ORANGE, stroke_width=2)
        
        self.play(Create(line_P1C), Create(line_P2C))
        self.wait(2)
        
        # 第7幕：总结
        summary = VGroup(
            Text("解析式: y = -4/3x² + 8/3x + 4", font_size=20, color=WHITE),
            Text("P₁(2, 4)", font_size=18, color=ORANGE),
            Text("P₂(7/3, 20/9)", font_size=18, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT)
        summary.to_edge(RIGHT)
        
        self.play(FadeOut(axes), FadeOut(parabola), FadeOut(line_BC), 
                  FadeOut(line_P1C), FadeOut(line_P2C),
                  FadeOut(A), FadeOut(B), FadeOut(C), FadeOut(P1), FadeOut(P2),
                  FadeOut(A_label), FadeOut(B_label), FadeOut(C_label), 
                  FadeOut(P1_label), FadeOut(P2_label),
                  FadeOut(symmetry_line), FadeOut(symmetry_label),
                  FadeOut(arrow1), FadeOut(arrow2))
        
        self.play(Write(summary))
        self.wait(3)
        
        self.play(FadeOut(summary))
