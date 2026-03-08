"""
几何旋转综合题 - 专业教学布局版
布局：
- 上部 30%：题目区域（左：已知条件，右：求解问题）
- 下部 70%：左右对半分（左：画图区域，右：讲解公式）
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
    """几何旋转综合题 - 专业教学布局版"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 查找音频目录
        self.audio_dir = Path(__file__).parent / "audio"
        if not self.audio_dir.exists():
            self.audio_dir = Path(__file__).parent.parent / "audio"
        
        # 加载音频时长
        self.audio_timings = self.load_audio_timings()
        
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
        """创建专业教学布局框架"""
        # 屏幕尺寸：16:9，宽度 14.22，高度 8
        # 留出安全边距：左右各 0.5
        safe_width = 13.22
        screen_height = 8
        
        # 上部 30%：题目区域
        title_height = screen_height * 0.3
        self.title_area = Rectangle(
            width=safe_width,
            height=title_height,
            color="#3498db",
            stroke_width=2
        )
        self.title_area.to_edge(UP, buff=0.2).shift(LEFT * 0.5)
        
        # 下部 70%：左右对半分
        bottom_height = screen_height * 0.7 - 0.2
        self.diagram_area = Rectangle(
            width=safe_width / 2 - 0.1,
            height=bottom_height,
            color="#2ecc71",
            stroke_width=2
        )
        self.diagram_area.next_to(self.title_area, DOWN, buff=0.1).align_to(self.title_area, LEFT).shift(DOWN * 0.1)
        
        self.formula_area = Rectangle(
            width=safe_width / 2 - 0.1,
            height=bottom_height,
            color="#e74c3c",
            stroke_width=2
        )
        self.formula_area.next_to(self.title_area, DOWN, buff=0.1).align_to(self.title_area, RIGHT).shift(DOWN * 0.1)
        
        # 标题文字（左对齐）
        self.title_text = Text("几何旋转综合题", font_size=36, color=WHITE)
        self.title_text.next_to(self.title_area, RIGHT, buff=0.5).align_to(self.title_area, UP).shift(DOWN * 0.5)
        
        # 初始隐藏所有框架（动态显示）
        self.layout_group = VGroup(
            self.title_area,
            self.diagram_area,
            self.formula_area
        )
    
    def show_layout(self, title_text=""):
        """显示布局框架"""
        self.play(FadeIn(self.title_area), FadeIn(self.diagram_area), FadeIn(self.formula_area))
        if title_text:
            new_title = Text(title_text, font_size=36, color=WHITE)
            new_title.move_to(self.title_area.get_center())
            self.play(FadeOut(self.title_text), FadeIn(new_title))
            self.title_text = new_title
    
    def hide_layout(self):
        """隐藏布局框架"""
        self.play(FadeOut(self.title_area), FadeOut(self.diagram_area), FadeOut(self.formula_area), FadeOut(self.title_text))
    
    def update_title(self, text):
        """更新标题文字"""
        new_title = Text(text, font_size=36, color=WHITE)
        new_title.move_to(self.title_area.get_center())
        self.play(Transform(self.title_text, new_title))
        self.title_text = new_title
    
    def add_to_diagram(self, *mobjects):
        """添加元素到画图区域"""
        for mob in mobjects:
            mob.move_to(self.diagram_area.get_center())
        self.play(*[FadeIn(mob) for mob in mobjects])
    
    def add_to_formula(self, *mobjects):
        """添加元素到公式区域"""
        formula_group = VGroup(*mobjects).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        formula_group.move_to(self.formula_area.get_center()).align_to(self.formula_area, LEFT).shift(RIGHT * 0.5)
        self.play(FadeIn(formula_group))
        return formula_group
    
    def create_triangle_ABC(self, scale=0.8):
        """创建 Rt△ABC"""
        # 定义点（按比例缩小以适应区域）
        C = ORIGIN
        B = RIGHT * 3 * scale  # BC = 3
        A = UP * 4 * scale     # AC = 4
        
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
        right_angle = RightAngle(line_AC, line_BC, length=0.3, color=RED)
        
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
        """第 1 幕：介绍题目"""
        self.add_scene_audio(1)
        
        start_time = self.time
        
        # 显示布局
        self.show_layout("已知条件")
        
        # 左侧：已知条件
        known_left = Tex(
            r"在 Rt$\triangle ABC$ 中：",
            font_size=28
        ).move_to(self.title_area.get_center()).shift(LEFT * 3.5 + DOWN * 0.5)
        
        known_right = Tex(
            r"$\angle ACB = 90^\circ$",
            r"$AC = 4$",
            r"$BC = 3$",
            font_size=24
        ).arrange(DOWN, buff=0.3).next_to(known_left, RIGHT, buff=1).align_to(known_left, UP)
        
        # 右侧：求解问题
        problem_title = Text("求解：", font_size=28, color="#f39c12").next_to(known_right, RIGHT, buff=2).align_to(known_left, UP)
        problem_list = Tex(
            r"(1) 求证：$\angle ABE = 90^\circ$",
            r"(2) 当 $D$ 为 $AB$ 中点时，求 $BE$",
            r"(3) 求证：$CE^2 = 2BD \cdot AD$，求 $CE$ 最小值",
            font_size=24,
            color="#2ecc71"
        ).arrange(DOWN, buff=0.3).next_to(problem_title, DOWN, buff=0.5).align_to(problem_title, LEFT)
        
        # 动画
        self.play(Write(known_left), Write(known_right))
        self.play(Write(problem_title), Write(problem_list))
        
        self.wait_for_audio(1, self.time - start_time)
        self.play(FadeOut(known_left), FadeOut(known_right), FadeOut(problem_title), FadeOut(problem_list))
    
    def scene_2_rotation(self):
        """第 2 幕：旋转动画"""
        self.add_scene_audio(2)
        
        start_time = self.time
        
        # 显示布局
        self.show_layout("旋转演示")
        
        # 左侧画图区域：创建三角形
        triangle, A, B, C = self.create_triangle_ABC(scale=0.6)
        triangle.move_to(self.diagram_area.get_center()).shift(LEFT * 0.5)
        
        # 右侧公式区域
        hint = Tex(
            r"思路：$\triangle CDE$ 可看作 $\triangle CDB$",
            r"绕点 $D$ 旋转 $90^\circ$ 得到",
            font_size=28,
            color="#f39c12"
        ).arrange(DOWN, buff=0.5).move_to(self.formula_area.get_center()).shift(RIGHT * 0.5)
        
        # 动画
        self.play(Create(triangle[0]))  # 三角形
        self.play(FadeIn(triangle[1:4]))  # 点
        self.play(FadeIn(triangle[4:7]))  # 标签
        
        # 创建点 D
        D = Line(A, B).point_from_proportion(0.6)
        dot_D = Dot(D, color=YELLOW)
        label_D = Text("D", font_size=20, color=YELLOW).next_to(dot_D, UR)
        self.play(FadeIn(dot_D), FadeIn(label_D))
        
        # 创建 CD
        line_CD = Line(C, D, color=YELLOW)
        self.play(Create(line_CD))
        
        # 旋转动画
        E = D + rotate_vector(C - D, PI/2)
        dot_E = Dot(E, color=GREEN)
        label_E = Text("E", font_size=20, color=GREEN).next_to(dot_E, DL)
        
        self.play(
            Rotate(line_CD, PI/2, about_point=D),
            FadeIn(dot_E),
            FadeIn(label_E),
            Write(hint[0]),
            run_time=2
        )
        
        line_DE = Line(D, E, color=GREEN)
        line_CE = Line(C, E, color=GREEN)
        self.play(Create(line_DE), Create(line_CE), Write(hint[1]))
        
        self.wait_for_audio(2, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(label_D), FadeOut(line_CD),
                  FadeOut(dot_E), FadeOut(label_E), FadeOut(line_DE), FadeOut(line_CE),
                  FadeOut(hint))
    
    def scene_3_proof(self):
        """第 3 幕：证明"""
        self.add_scene_audio(3)
        
        start_time = self.time
        
        # 显示布局
        self.show_layout("证明：∠ABE = 90°")
        
        # 左侧：几何图形
        triangle, A, B, C = self.create_triangle_ABC(scale=0.5)
        triangle.move_to(self.diagram_area.get_center()).shift(LEFT * 1)
        
        D = Line(A, B).point_from_proportion(0.6)
        E = D + rotate_vector(C - D, PI/2)
        
        dot_D = Dot(D, color=YELLOW)
        dot_E = Dot(E, color=GREEN)
        line_BE = Line(B, E, color=RED)
        
        # 高亮三角形
        triangle_ACD = Polygon(A, C, D, color=BLUE, fill_opacity=0.4)
        triangle_BED = Polygon(B, E, D, color=GREEN, fill_opacity=0.4)
        
        self.add(triangle, dot_D, dot_E, line_BE)
        
        # 右侧：证明步骤
        step1 = Tex(r"在 $\triangle ACD$ 和 $\triangle BED$ 中：", font_size=24)
        step2 = Tex(r"$CD = DE$（已知）", font_size=22)
        step3 = Tex(r"$\angle ADC = \angle BDE$（对顶角）", font_size=22)
        step4 = Tex(r"$\angle ACD = \angle BDE$（旋转）", font_size=22)
        
        proof_group = VGroup(step1, step2, step3, step4).arrange(DOWN, buff=0.3)
        proof_group.move_to(self.formula_area.get_center()).shift(RIGHT * 0.5).align_to(self.formula_area, UP).shift(DOWN * 0.5)
        
        congruent = Tex(r"$\therefore \triangle ACD \cong \triangle BED$（SAS）", font_size=24, color="#f39c12")
        congruent.next_to(proof_group, DOWN, buff=0.5).align_to(proof_group, LEFT)
        
        final = Tex(r"$\therefore \angle ABE = 90^\circ$", font_size=28, color="#2ecc71")
        final.next_to(congruent, DOWN, buff=0.5).align_to(congruent, LEFT)
        
        # 动画
        self.play(FadeIn(triangle_ACD), FadeIn(triangle_BED))
        self.play(Write(proof_group))
        self.play(Write(congruent))
        self.play(Write(final))
        
        self.wait_for_audio(3, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(dot_E), FadeOut(line_BE),
                  FadeOut(triangle_ACD), FadeOut(triangle_BED), FadeOut(proof_group),
                  FadeOut(congruent), FadeOut(final))
    
    def scene_4_q2(self):
        """第 4 幕：第 2 问"""
        self.add_scene_audio(4)
        
        start_time = self.time
        
        # 显示布局
        self.show_layout("第 (2) 问：D 为 AB 中点")
        
        # 左侧：几何图形（D 为中点）
        triangle, A, B, C = self.create_triangle_ABC(scale=0.5)
        triangle.move_to(self.diagram_area.get_center()).shift(LEFT * 1)
        
        D = Line(A, B).point_from_proportion(0.5)  # 中点
        E = D + rotate_vector(C - D, PI/2)
        
        dot_D = Dot(D, color=YELLOW)
        label_D = Text("D（中点）", font_size=18, color=YELLOW).next_to(dot_D, UR)
        dot_E = Dot(E, color=GREEN)
        line_BE = Line(B, E, color=RED)
        
        self.add(triangle, dot_D, label_D, dot_E, line_BE)
        
        # 右侧：提示
        hint = Tex(
            r"由（1）知：$\triangle ACD \cong \triangle BED$",
            r"$\therefore BE = AC = 4$",
            font_size=28,
            color="#2ecc71"
        ).arrange(DOWN, buff=0.5).move_to(self.formula_area.get_center()).shift(RIGHT * 0.5)
        
        self.play(Write(hint))
        
        self.wait_for_audio(4, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(label_D), FadeOut(dot_E),
                  FadeOut(line_BE), FadeOut(hint))
    
    def scene_5_q2_calc(self):
        """第 5 幕：第 2 问计算"""
        self.add_scene_audio(5)
        
        start_time = self.time
        
        # 显示布局
        self.show_layout("计算过程")
        
        # 左侧：空白（或简单图形）
        placeholder = Text("图形见左侧", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.diagram_area.get_center())
        self.play(Write(placeholder))
        
        # 右侧：计算步骤
        step1_title = Text("步骤 1：求 AB", font_size=26, color="#3498db")
        pythagoras = Tex(r"$AB^2 = AC^2 + BC^2 = 4^2 + 3^2 = 25$", font_size=24)
        result1 = Tex(r"$\therefore AB = 5$", font_size=24)
        
        step2_title = Text("步骤 2：求 AD、BD", font_size=26, color="#3498db")
        midpoint = Tex(r"$\because D$ 是 $AB$ 中点", font_size=22)
        result2 = Tex(r"$\therefore AD = BD = 2.5$", font_size=24)
        
        step3_title = Text("步骤 3：求 BE", font_size=26, color="#3498db")
        congruent = Tex(r"由（1）：$\triangle ACD \cong \triangle BED$", font_size=22)
        final = Tex(r"$\therefore BE = AC = 4$", font_size=28, color="#2ecc71")
        
        calc_group = VGroup(
            step1_title, pythagoras, result1,
            step2_title, midpoint, result2,
            step3_title, congruent, final
        ).arrange(DOWN, buff=0.3)
        calc_group.move_to(self.formula_area.get_center()).shift(RIGHT * 0.5).align_to(self.formula_area, UP).shift(DOWN * 0.3)
        
        self.play(Write(calc_group))
        
        self.wait_for_audio(5, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(calc_group))
    
    def scene_6_q3_similar(self):
        """第 6 幕：第 3 问①相似"""
        self.add_scene_audio(6)
        
        start_time = self.time
        
        # 显示布局
        self.show_layout("第 (3) 问①：相似三角形")
        
        # 左侧：几何图形
        triangle, A, B, C = self.create_triangle_ABC(scale=0.5)
        triangle.move_to(self.diagram_area.get_center()).shift(LEFT * 1)
        
        D = Line(A, B).point_from_proportion(0.6)
        E = D + rotate_vector(C - D, PI/2)
        
        dot_D = Dot(D, color=YELLOW)
        dot_E = Dot(E, color=GREEN)
        line_CD = Line(C, D, color=YELLOW)
        line_DE = Line(D, E, color=GREEN)
        line_CE = Line(C, E, color=GREEN)
        
        # 高亮相似三角形
        triangle_ACD = Polygon(A, C, D, color=BLUE, fill_opacity=0.3)
        triangle_CBD = Polygon(C, B, D, color=RED, fill_opacity=0.3)
        
        self.add(triangle, dot_D, dot_E, line_CD, line_DE, line_CE)
        
        # 右侧：提示
        hint = Tex(
            r"关键：证明 $\triangle ACD \sim \triangle CBD$",
            font_size=26,
            color="#f39c12"
        ).move_to(self.formula_area.get_center()).shift(RIGHT * 0.5)
        
        self.play(FadeIn(triangle_ACD), FadeIn(triangle_CBD), Write(hint))
        
        self.wait_for_audio(6, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(dot_E), FadeOut(line_CD),
                  FadeOut(line_DE), FadeOut(line_CE), FadeOut(triangle_ACD),
                  FadeOut(triangle_CBD), FadeOut(hint))
    
    def scene_7_q3_proof(self):
        """第 7 幕：第 3 问①证明"""
        self.add_scene_audio(7)
        
        start_time = self.time
        
        # 显示布局
        self.show_layout("证明：CE² = 2BD·AD")
        
        # 左侧：空白
        placeholder = Text("图形辅助", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.diagram_area.get_center())
        self.play(Write(placeholder))
        
        # 右侧：证明步骤
        step1 = Tex(r"在 Rt$\triangle CDE$ 中：", font_size=24)
        pythagoras = Tex(r"$CE^2 = CD^2 + DE^2 = 2CD^2$", font_size=24)
        
        step2 = Tex(r"证明 $CD^2 = BD \cdot AD$：", font_size=24)
        similar = Tex(r"$\triangle ACD \sim \triangle CBD$（AA）", font_size=22)
        ratio = Tex(r"$\therefore \frac{AD}{CD} = \frac{CD}{BD}$", font_size=22)
        result = Tex(r"即 $CD^2 = BD \cdot AD$", font_size=22)
        
        final = Tex(r"$\therefore CE^2 = 2CD^2 = 2BD \cdot AD$", font_size=26, color="#2ecc71")
        
        proof_group = VGroup(
            step1, pythagoras,
            step2, similar, ratio, result,
            final
        ).arrange(DOWN, buff=0.3)
        proof_group.move_to(self.formula_area.get_center()).shift(RIGHT * 0.5).align_to(self.formula_area, UP).shift(DOWN * 0.3)
        
        self.play(Write(proof_group))
        
        self.wait_for_audio(7, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(proof_group))
    
    def scene_8_q3_minimum(self):
        """第 8 幕：第 3 问②最小值"""
        self.add_scene_audio(8)
        
        start_time = self.time
        
        # 显示布局
        self.show_layout("求 CE 最小值")
        
        # 左侧：函数图像占位
        placeholder = Text("函数图像", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.diagram_area.get_center())
        self.play(Write(placeholder))
        
        # 右侧：函数推导
        step1 = Tex(r"由①：$CE^2 = 2BD \cdot AD$", font_size=24)
        step2 = Tex(r"设 $AD = x$，则 $BD = 5 - x$", font_size=22)
        function = Tex(r"$CE^2 = 2(5-x)x = -2x^2 + 10x$", font_size=24)
        analysis = Tex(r"二次函数，开口向下，有最大值", font_size=22)
        vertex = Tex(r"当 $x = 2.5$ 时，$CE^2_{max} = 12.5$", font_size=22)
        final = Tex(r"$\therefore CE_{min} = \sqrt{12.5} = \frac{5\sqrt{2}}{2}$", font_size=26, color="#2ecc71")
        
        calc_group = VGroup(
            step1, step2, function, analysis, vertex, final
        ).arrange(DOWN, buff=0.3)
        calc_group.move_to(self.formula_area.get_center()).shift(RIGHT * 0.5).align_to(self.formula_area, UP).shift(DOWN * 0.3)
        
        self.play(Write(calc_group))
        
        self.wait_for_audio(8, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(calc_group))
    
    def scene_9_summary(self):
        """第 9 幕：答案汇总"""
        self.add_scene_audio(9)
        
        start_time = self.time
        
        # 显示布局
        self.show_layout("答案汇总")
        
        # 左侧：空白
        placeholder = Text("回顾图形", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.diagram_area.get_center())
        self.play(Write(placeholder))
        
        # 右侧：答案和方法
        ans1 = Tex(r"(1) $\triangle ACD \cong \triangle BED$（SAS）", font_size=22)
        ans1_result = Tex(r"$\therefore \angle ABE = 90^\circ$", font_size=22)
        
        ans2 = Tex(r"(2) $BE = 4$", font_size=26, color="#2ecc71")
        
        ans3_1 = Tex(r"(3) ① $CE^2 = 2BD \cdot AD$", font_size=22)
        ans3_2 = Tex(r"② $CE_{min} = \frac{5\sqrt{2}}{2}$", font_size=26, color="#2ecc71")
        
        method_title = Text("解题方法：", font_size=26, color="#f39c12")
        method1 = Text("1. 旋转全等 → 证明垂直", font_size=20)
        method2 = Text("2. 勾股定理 → 求边长", font_size=20)
        method3 = Text("3. 相似三角形 → 建立关系", font_size=20)
        method4 = Text("4. 二次函数 → 求最值", font_size=20)
        
        thanks = Text("谢谢观看！", font_size=36, color="#3498db")
        
        summary_group = VGroup(
            ans1, ans1_result, ans2, ans3_1, ans3_2,
            method_title, method1, method2, method3, method4,
            thanks
        ).arrange(DOWN, buff=0.3)
        summary_group.move_to(self.formula_area.get_center()).shift(RIGHT * 0.5)
        
        self.play(Write(summary_group))
        
        self.wait_for_audio(9, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(summary_group),
                  FadeOut(self.title_area), FadeOut(self.diagram_area), FadeOut(self.formula_area))


if __name__ == "__main__":
    scene = GeometryRotationProblem()
    scene.render()
