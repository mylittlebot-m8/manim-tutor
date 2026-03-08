"""
几何旋转综合题 - 精确定位布局版 v4
修复：
1. 第 1 幕：已知/求解 Y 坐标往下调 20%
2. 所有公式内容 trim（两边空白）
3. 后面标题显示时，前面标题隐藏（避免叠加）
"""

from manim import *
import json
from pathlib import Path

# ========== xelatex 中文支持 ==========
config.tex_compiler = "xelatex"
template = TexTemplate()
template.tex_compiler = "xelatex"
template.output_format = ".xdv"
template.add_to_preamble(r"\usepackage{xeCJK}")
template.add_to_preamble(r"\setCJKmainfont{WenQuanYi Zen Hei}")
config.tex_template = template
# ====================================


class GeometryRotationProblem(Scene):
    """几何旋转综合题 - 精确定位布局版 v4"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 查找音频目录
        self.audio_dir = Path(__file__).parent / "audio"
        if not self.audio_dir.exists():
            self.audio_dir = Path(__file__).parent.parent / "audio"
        
        # 加载音频时长
        self.audio_timings = self.load_audio_timings()
        
        # 定义精确布局（16:9 屏幕，1920x1080）
        # 标题框：18% 高度，留出字幕空间
        self.TITLE_HEIGHT = 1.8  # 18% of 10
        self.TITLE_Y = 4.1  # 标题中心 Y 坐标
        
        # 下部 82%：左右对半分
        self.DIAGRAM_CENTER = LEFT * 4.75 + DOWN * 1.5  # 画图区域中心
        self.FORMULA_CENTER = RIGHT * 4.75 + DOWN * 1.5  # 公式区域中心
        
        # 第 1 幕内容位置（往下调 20%，往中间调）
        self.KNOWN_POS = LEFT * 3.5 + UP * 1.6  # 已知条件位置（往下调 20%）
        self.PROBLEM_POS = RIGHT * 3.5 + UP * 1.6  # 求解问题位置（往下调 20%）
        
        # 创建布局框架
        self.create_layout()
        
        # 9 幕内容
        self.scene_1_intro()
        self.scene_2_rotation()
        self.scene_3_proof()
        self.scene_4_q2()
        self.scene_5_q2_calc()
        self.scene_6_q3_similar()
        self.scene_7_q3_proof()
        self.scene_8_q3_minimum()
        self.scene_9_summary()
    
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
    
    def create_layout(self):
        """创建精确布局框架"""
        # 上部 18%：标题区域
        self.title_box = Rectangle(
            width=18,  # 留边距
            height=self.TITLE_HEIGHT,
            color="#3498db",
            stroke_width=2
        )
        self.title_box.to_edge(UP, buff=0.2)
        
        # 下部左侧：画图区域
        self.diagram_box = Rectangle(
            width=9.0,
            height=6.5,
            color="#2ecc71",
            stroke_width=2
        )
        self.diagram_box.move_to(self.DIAGRAM_CENTER)
        
        # 下部右侧：公式区域
        self.formula_box = Rectangle(
            width=9.0,
            height=6.5,
            color="#e74c3c",
            stroke_width=2
        )
        self.formula_box.move_to(self.FORMULA_CENTER)
        
        # 初始隐藏
        self.layout_group = VGroup(self.title_box, self.diagram_box, self.formula_box)
    
    def show_layout(self, title_text=""):
        """显示布局框架（自动隐藏上一个标题）"""
        self.play(FadeIn(self.title_box), FadeIn(self.diagram_box), FadeIn(self.formula_box))
        if title_text:
            # 隐藏上一个标题
            if hasattr(self, 'title_text') and self.title_text:
                self.play(FadeOut(self.title_text))
            
            # 标题在画图区域上方
            new_title = Text(title_text.strip(), font_size=32, color=WHITE)
            new_title.move_to(self.DIAGRAM_CENTER + UP * 3.5)
            self.play(FadeIn(new_title))
            self.title_text = new_title
    
    def hide_layout(self):
        """隐藏布局框架"""
        fade_out_list = [self.title_box, self.diagram_box, self.formula_box]
        if hasattr(self, 'title_text') and self.title_text:
            fade_out_list.append(self.title_text)
        self.play(FadeOut(*fade_out_list))
    
    def update_title(self, text):
        """更新标题文字"""
        if hasattr(self, 'title_text') and self.title_text:
            new_title = Text(text.strip(), font_size=32, color=WHITE)
            new_title.move_to(self.DIAGRAM_CENTER + UP * 3.5)
            self.play(Transform(self.title_text, new_title))
            self.title_text = new_title
    
    def create_triangle_ABC(self, scale=0.7):
        """创建 Rt△ABC（严格限制在左侧区域）"""
        # 定义点（缩小以适应左侧区域）
        C = self.DIAGRAM_CENTER
        B = self.DIAGRAM_CENTER + RIGHT * 2.5 * scale
        A = self.DIAGRAM_CENTER + UP * 3.5 * scale
        
        # 创建三角形
        triangle = Polygon(A, B, C, color=BLUE, fill_opacity=0.3)
        
        # 创建点
        dot_A = Dot(A, color=WHITE)
        dot_B = Dot(B, color=WHITE)
        dot_C = Dot(C, color=WHITE)
        
        # 创建标签
        label_A = Text("A", font_size=24).next_to(A, UP)
        label_B = Text("B", font_size=24).next_to(B, RIGHT)
        label_C = Text("C", font_size=24).next_to(C, DL)
        
        # 直角标记
        line_AC = Line(A, C)
        line_BC = Line(B, C)
        right_angle = RightAngle(line_AC, line_BC, length=0.25, color=RED)
        
        # 边长标注
        label_AC = Text("4", font_size=20, color=GREEN).next_to(line_AC, LEFT)
        label_BC = Text("3", font_size=20, color=GREEN).next_to(line_BC, DOWN)
        
        return VGroup(
            triangle,
            dot_A, dot_B, dot_C,
            label_A, label_B, label_C,
            right_angle,
            label_AC, label_BC
        ), A, B, C
    
    def scene_1_intro(self):
        """第 1 幕：读题（全屏显示，左右分开，Y 坐标往下调 20%）"""
        self.add_scene_audio(1)
        
        start_time = self.time
        
        # 第 1 幕不显示布局框，直接显示内容
        # 标题
        main_title = Text("几何旋转综合题", font_size=40, color=WHITE)
        main_title.to_edge(UP, buff=0.5)
        
        # 左侧：已知条件（严格左对齐，Y 坐标往下调 20%）
        known = Tex(
            r"\textbf{已知：}",
            r"在 Rt$\triangle ABC$ 中",
            r"$\angle ACB = 90^\circ$",
            r"$AC = 4$",
            r"$BC = 3$",
            font_size=28
        ).arrange(DOWN, buff=0.4)
        known.move_to(self.KNOWN_POS)
        
        # 右侧：求解问题（严格右对齐，往中间调，避免太靠右）
        problem = Tex(
            r"\textbf{求解：}",
            r"(1) 求证：$\angle ABE = 90^\circ$",
            r"(2) 当 $D$ 为 $AB$ 中点时，求 $BE$",
            r"(3) $CE^2 = 2BD \cdot AD$，求 $CE$ 最小值",
            font_size=24,
            color="#2ecc71"
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        problem.move_to(self.PROBLEM_POS)
        
        self.play(Write(main_title))
        self.play(Write(known), Write(problem))
        self.wait_for_audio(1, self.time - start_time)
        self.play(FadeOut(main_title), FadeOut(known), FadeOut(problem))
    
    def scene_2_rotation(self):
        """第 2 幕：旋转动画（显示布局框）"""
        self.add_scene_audio(2)
        
        start_time = self.time
        self.show_layout("旋转演示")  # 标题在框内居中
        
        # 左侧：三角形（严格在左侧区域）
        triangle, A, B, C = self.create_triangle_ABC(scale=0.6)
        self.play(Create(triangle[0]))
        self.play(FadeIn(triangle[1:7]))
        
        # 点 D
        D = Line(A, B).point_from_proportion(0.6)
        dot_D = Dot(D, color=YELLOW)
        label_D = Text("D", font_size=20, color=YELLOW).next_to(dot_D, UR)
        self.play(FadeIn(dot_D), FadeIn(label_D))
        
        # 线段 CD
        line_CD = Line(C, D, color=YELLOW)
        self.play(Create(line_CD))
        
        # 右侧：提示（严格在右侧区域）
        hint = Tex(
            r"\textbf{思路：}",
            r"$\triangle CDE$ 可看作 $\triangle CDB$",
            r"绕点 $D$ 旋转 $90^\circ$ 得到",
            font_size=26,
            color="#f39c12"
        ).arrange(DOWN, buff=0.5)
        hint.move_to(self.FORMULA_CENTER)
        self.play(Write(hint))
        
        # 旋转动画
        E = D + rotate_vector(C - D, PI/2)
        dot_E = Dot(E, color=GREEN)
        label_E = Text("E", font_size=20, color=GREEN).next_to(dot_E, DL)
        
        self.play(
            Rotate(line_CD, PI/2, about_point=D),
            FadeIn(dot_E),
            FadeIn(label_E),
            run_time=2
        )
        
        line_DE = Line(D, E, color=GREEN)
        line_CE = Line(C, E, color=GREEN)
        self.play(Create(line_DE), Create(line_CE))
        
        self.wait_for_audio(2, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(label_D), FadeOut(line_CD),
                  FadeOut(dot_E), FadeOut(label_E), FadeOut(line_DE), FadeOut(line_CE),
                  FadeOut(hint))
    
    def scene_3_proof(self):
        """第 3 幕：证明"""
        self.add_scene_audio(3)
        
        start_time = self.time
        self.show_layout("证明：∠ABE = 90°")
        
        # 左侧：几何图形
        triangle, A, B, C = self.create_triangle_ABC(scale=0.5)
        D = Line(A, B).point_from_proportion(0.6)
        E = D + rotate_vector(C - D, PI/2)
        
        dot_D = Dot(D, color=YELLOW)
        dot_E = Dot(E, color=GREEN)
        line_BE = Line(B, E, color=RED)
        
        triangle_ACD = Polygon(A, C, D, color=BLUE, fill_opacity=0.4)
        triangle_BED = Polygon(B, E, D, color=GREEN, fill_opacity=0.4)
        
        self.add(triangle, dot_D, dot_E, line_BE)
        self.play(FadeIn(triangle_ACD), FadeIn(triangle_BED))
        
        # 右侧：证明步骤（严格右对齐，trim 空白）
        proof = Tex(
            r"在 $\triangle ACD$ 和 $\triangle BED$ 中：",
            r"$CD = DE$（已知）",
            r"$\angle ADC = \angle BDE$（对顶角）",
            r"$\angle ACD = \angle BDE$（旋转）",
            r"$\therefore \triangle ACD \cong \triangle BED$（SAS）",
            r"$\therefore \angle ABE = 90^\circ$",
            font_size=24
        ).arrange(DOWN, buff=0.3)
        proof[-1].set_color("#2ecc71")
        proof.move_to(self.FORMULA_CENTER)
        
        self.play(Write(proof))
        self.wait_for_audio(3, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(dot_E), FadeOut(line_BE),
                  FadeOut(triangle_ACD), FadeOut(triangle_BED), FadeOut(proof))
    
    def scene_4_q2(self):
        """第 4 幕：第 2 问"""
        self.add_scene_audio(4)
        
        start_time = self.time
        self.show_layout("第 (2) 问：D 为 AB 中点")
        
        # 左侧：图形
        triangle, A, B, C = self.create_triangle_ABC(scale=0.5)
        D = Line(A, B).point_from_proportion(0.5)
        E = D + rotate_vector(C - D, PI/2)
        
        dot_D = Dot(D, color=YELLOW)
        label_D = Text("D（中点）", font_size=18, color=YELLOW).next_to(dot_D, UR)
        dot_E = Dot(E, color=GREEN)
        line_BE = Line(B, E, color=RED)
        
        self.add(triangle, dot_D, label_D, dot_E, line_BE)
        
        # 右侧：结论
        result = Tex(
            r"由（1）：$\triangle ACD \cong \triangle BED$",
            r"$\therefore BE = AC = 4$",
            font_size=32,
            color="#2ecc71"
        ).arrange(DOWN, buff=0.5)
        result.move_to(self.FORMULA_CENTER)
        
        self.play(Write(result))
        self.wait_for_audio(4, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(label_D), FadeOut(dot_E),
                  FadeOut(line_BE), FadeOut(result))
    
    def scene_5_q2_calc(self):
        """第 5 幕：计算过程"""
        self.add_scene_audio(5)
        
        start_time = self.time
        self.show_layout("计算过程")
        
        # 左侧：占位
        placeholder = Text("图形辅助", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.DIAGRAM_CENTER)
        self.play(Write(placeholder))
        
        # 右侧：计算步骤（严格右对齐，trim 空白）
        calc = Tex(
            r"\textbf{步骤 1：求 AB}",
            r"$AB^2 = AC^2 + BC^2 = 4^2 + 3^2 = 25$",
            r"$\therefore AB = 5$",
            r"",
            r"\textbf{步骤 2：求 AD、BD}",
            r"$\because D$ 是 $AB$ 中点",
            r"$\therefore AD = BD = 2.5$",
            r"",
            r"\textbf{步骤 3：求 BE}",
            r"由（1）：$\triangle ACD \cong \triangle BED$",
            r"$\therefore BE = AC = 4$",
            font_size=24
        ).arrange(DOWN, buff=0.3)
        calc[-1].set_color("#2ecc71")
        calc.move_to(self.FORMULA_CENTER)
        
        self.play(Write(calc))
        self.wait_for_audio(5, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(calc))
    
    def scene_6_q3_similar(self):
        """第 6 幕：相似三角形"""
        self.add_scene_audio(6)
        
        start_time = self.time
        self.show_layout("第 (3) 问①：相似三角形")
        
        # 左侧：图形
        triangle, A, B, C = self.create_triangle_ABC(scale=0.5)
        D = Line(A, B).point_from_proportion(0.6)
        E = D + rotate_vector(C - D, PI/2)
        
        dot_D = Dot(D, color=YELLOW)
        dot_E = Dot(E, color=GREEN)
        line_CD = Line(C, D, color=YELLOW)
        line_DE = Line(D, E, color=GREEN)
        line_CE = Line(C, E, color=GREEN)
        
        triangle_ACD = Polygon(A, C, D, color=BLUE, fill_opacity=0.3)
        triangle_CBD = Polygon(C, B, D, color=RED, fill_opacity=0.3)
        
        self.add(triangle, dot_D, dot_E, line_CD, line_DE, line_CE)
        self.play(FadeIn(triangle_ACD), FadeIn(triangle_CBD))
        
        # 右侧：提示
        hint = Tex(
            r"\textbf{关键：}",
            r"证明 $\triangle ACD \sim \triangle CBD$",
            font_size=28,
            color="#f39c12"
        ).arrange(DOWN, buff=0.5)
        hint.move_to(self.FORMULA_CENTER)
        
        self.play(Write(hint))
        self.wait_for_audio(6, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(dot_E), FadeOut(line_CD),
                  FadeOut(line_DE), FadeOut(line_CE), FadeOut(triangle_ACD),
                  FadeOut(triangle_CBD), FadeOut(hint))
    
    def scene_7_q3_proof(self):
        """第 7 幕：证明"""
        self.add_scene_audio(7)
        
        start_time = self.time
        self.show_layout("证明：CE² = 2BD·AD")
        
        # 左侧：占位
        placeholder = Text("图形辅助", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.DIAGRAM_CENTER)
        self.play(Write(placeholder))
        
        # 右侧：证明（严格右对齐，trim 空白）
        proof = Tex(
            r"在 Rt$\triangle CDE$ 中：",
            r"$CE^2 = CD^2 + DE^2 = 2CD^2$",
            r"",
            r"\textbf{证明 $CD^2 = BD \cdot AD$：}",
            r"$\triangle ACD \sim \triangle CBD$（AA）",
            r"$\therefore \frac{AD}{CD} = \frac{CD}{BD}$",
            r"即 $CD^2 = BD \cdot AD$",
            r"",
            r"$\therefore CE^2 = 2CD^2 = 2BD \cdot AD$",
            font_size=24
        ).arrange(DOWN, buff=0.3)
        proof[-1].set_color("#2ecc71")
        proof.move_to(self.FORMULA_CENTER)
        
        self.play(Write(proof))
        self.wait_for_audio(7, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(proof))
    
    def scene_8_q3_minimum(self):
        """第 8 幕：最小值"""
        self.add_scene_audio(8)
        
        start_time = self.time
        self.show_layout("求 CE 最小值")
        
        # 左侧：占位
        placeholder = Text("函数图像", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.DIAGRAM_CENTER)
        self.play(Write(placeholder))
        
        # 右侧：函数推导（严格右对齐，trim 空白）
        calc = Tex(
            r"由①：$CE^2 = 2BD \cdot AD$",
            r"设 $AD = x$，则 $BD = 5 - x$",
            r"$CE^2 = 2(5-x)x = -2x^2 + 10x$",
            r"",
            r"二次函数，开口向下，有最大值",
            r"当 $x = 2.5$ 时，$CE^2_{max} = 12.5$",
            r"",
            r"$\therefore CE_{min} = \sqrt{12.5} = \frac{5\sqrt{2}}{2}$",
            font_size=24
        ).arrange(DOWN, buff=0.3)
        calc[-1].set_color("#2ecc71")
        calc.move_to(self.FORMULA_CENTER)
        
        self.play(Write(calc))
        self.wait_for_audio(8, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(calc))
    
    def scene_9_summary(self):
        """第 9 幕：答案汇总"""
        self.add_scene_audio(9)
        
        start_time = self.time
        self.show_layout("答案汇总")
        
        # 左侧：占位
        placeholder = Text("回顾图形", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.DIAGRAM_CENTER)
        self.play(Write(placeholder))
        
        # 右侧：答案和方法（严格右对齐，trim 空白）
        summary = Tex(
            r"\textbf{答案：}",
            r"(1) $\triangle ACD \cong \triangle BED$（SAS）$\Rightarrow \angle ABE = 90^\circ$",
            r"(2) $BE = 4$",
            r"(3) ① $CE^2 = 2BD \cdot AD$",
            r"② $CE_{min} = \frac{5\sqrt{2}}{2}$",
            r"",
            r"\textbf{解题方法：}",
            r"1. 旋转全等 → 证明垂直",
            r"2. 勾股定理 → 求边长",
            r"3. 相似三角形 → 建立关系",
            r"4. 二次函数 → 求最值",
            r"",
            r"\textbf{谢谢观看！}",
            font_size=22
        ).arrange(DOWN, buff=0.25)
        summary[-1].set_color("#3498db")
        summary[-1].set_font_size(32)
        summary.move_to(self.FORMULA_CENTER)
        
        self.play(Write(summary))
        self.wait_for_audio(9, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(summary),
                  FadeOut(self.title_box), FadeOut(self.diagram_box), FadeOut(self.formula_box))


if __name__ == "__main__":
    scene = GeometryRotationProblem()
    scene.render()
