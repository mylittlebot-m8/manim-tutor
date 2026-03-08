"""
几何旋转综合题 - 精确定位布局版 v7
修复 Tex 格式错误：使用 MathTex 分开写
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
    """几何旋转综合题 - 精确定位布局版 v7"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        self.audio_dir = Path(__file__).parent / "audio"
        if not self.audio_dir.exists():
            self.audio_dir = Path(__file__).parent.parent / "audio"
        
        self.audio_timings = self.load_audio_timings()
        
        self.TITLE_HEIGHT = 1.8
        self.DIAGRAM_CENTER = LEFT * 4.75 + DOWN * 1.4
        self.FORMULA_CENTER = RIGHT * 4.75 + DOWN * 1.4
        self.KNOWN_POS = LEFT * 3.5 + DOWN * 0.5
        self.PROBLEM_POS = RIGHT * 3.5 + DOWN * 0.5
        self.TITLE_POS = self.DIAGRAM_CENTER + UP * 3.5
        
        self.create_layout()
        
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
        self.title_box = Rectangle(width=18, height=self.TITLE_HEIGHT, color="#3498db", stroke_width=2)
        self.title_box.to_edge(UP, buff=0.2)
        
        self.diagram_box = Rectangle(width=9.0, height=6.5, color="#2ecc71", stroke_width=2)
        self.diagram_box.move_to(self.DIAGRAM_CENTER)
        
        self.formula_box = Rectangle(width=9.0, height=6.5, color="#e74c3c", stroke_width=2)
        self.formula_box.move_to(self.FORMULA_CENTER)
        
        self.layout_group = VGroup(self.title_box, self.diagram_box, self.formula_box)
    
    def show_layout(self, title_text=""):
        self.play(FadeIn(self.title_box), FadeIn(self.diagram_box), FadeIn(self.formula_box))
        if title_text:
            if hasattr(self, 'title_text') and self.title_text:
                self.play(FadeOut(self.title_text))
            new_title = Text(title_text.strip(), font_size=32, color=WHITE)
            new_title.move_to(self.TITLE_POS)
            self.play(FadeIn(new_title))
            self.title_text = new_title
    
    def hide_layout(self):
        fade_out_list = [self.title_box, self.diagram_box, self.formula_box]
        if hasattr(self, 'title_text') and self.title_text:
            fade_out_list.append(self.title_text)
        self.play(FadeOut(*fade_out_list))
    
    def update_title(self, text):
        if hasattr(self, 'title_text') and self.title_text:
            new_title = Text(text.strip(), font_size=32, color=WHITE)
            new_title.move_to(self.TITLE_POS)
            self.play(Transform(self.title_text, new_title))
            self.title_text = new_title
    
    def create_triangle_ABC(self, scale=0.7):
        C = self.DIAGRAM_CENTER
        B = self.DIAGRAM_CENTER + RIGHT * 2.5 * scale
        A = self.DIAGRAM_CENTER + UP * 3.5 * scale
        
        triangle = Polygon(A, B, C, color=BLUE, fill_opacity=0.3)
        
        dot_A = Dot(A, color=WHITE)
        dot_B = Dot(B, color=WHITE)
        dot_C = Dot(C, color=WHITE)
        
        label_A = Text("A", font_size=24).next_to(A, UP)
        label_B = Text("B", font_size=24).next_to(B, RIGHT)
        label_C = Text("C", font_size=24).next_to(C, DL)
        
        line_AC = Line(A, C)
        line_BC = Line(B, C)
        right_angle = RightAngle(line_AC, line_BC, length=0.25, color=RED)
        
        label_AC = Text("4", font_size=20, color=GREEN).next_to(line_AC, LEFT)
        label_BC = Text("3", font_size=20, color=GREEN).next_to(line_BC, DOWN)
        
        return VGroup(triangle, dot_A, dot_B, dot_C, label_A, label_B, label_C, right_angle, label_AC, label_BC), A, B, C
    
    def scene_1_intro(self):
        self.add_scene_audio(1)
        start_time = self.time
        
        main_title = Text("几何旋转综合题", font_size=40, color=WHITE)
        main_title.to_edge(UP, buff=0.5)
        
        known = VGroup(
            Text("已知：", font_size=28, color=WHITE),
            Text("在 Rt△ABC 中", font_size=28, color=WHITE),
            MathTex(r"\angle ACB = 90^\circ", font_size=28),
            MathTex(r"AC = 4", font_size=28),
            MathTex(r"BC = 3", font_size=28)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        known.move_to(self.KNOWN_POS)
        
        problem = VGroup(
            Text("求解：", font_size=28, color="#2ecc71"),
            MathTex(r"(1)\ \angle ABE = 90^\circ", font_size=28, color="#2ecc71"),
            MathTex(r"(2)\ D\text{为}AB\text{中点，求}BE", font_size=28, color="#2ecc71"),
            MathTex(r"(3)\ CE^2 = 2BD \cdot CD\text{，求}CE\text{最小值}", font_size=28, color="#2ecc71")
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        problem.move_to(self.PROBLEM_POS)
        
        self.play(Write(main_title))
        self.play(Write(known), Write(problem))
        self.wait_for_audio(1, self.time - start_time)
        self.play(FadeOut(main_title), FadeOut(known), FadeOut(problem))
    
    def scene_2_rotation(self):
        self.add_scene_audio(2)
        start_time = self.time
        self.show_layout("旋转演示")
        
        triangle, A, B, C = self.create_triangle_ABC(scale=0.6)
        self.play(Create(triangle[0]))
        self.play(FadeIn(triangle[1:7]))
        
        D = Line(A, B).point_from_proportion(0.6)
        dot_D = Dot(D, color=YELLOW)
        label_D = Text("D", font_size=20, color=YELLOW).next_to(dot_D, UR)
        self.play(FadeIn(dot_D), FadeIn(label_D))
        
        line_CD = Line(C, D, color=YELLOW)
        self.play(Create(line_CD))
        
        hint = VGroup(
            Text("思路：", font_size=26, color="#f39c12"),
            MathTex(r"\triangle CDE\text{可看作}\triangle CDB", font_size=26, color="#f39c12"),
            MathTex(r"\text{绕点}D\text{旋转}90^\circ\text{得到}", font_size=26, color="#f39c12")
        ).arrange(DOWN, buff=0.5)
        hint.move_to(self.FORMULA_CENTER)
        self.play(Write(hint))
        
        E = D + rotate_vector(C - D, PI/2)
        dot_E = Dot(E, color=GREEN)
        label_E = Text("E", font_size=20, color=GREEN).next_to(dot_E, DL)
        
        self.play(Rotate(line_CD, PI/2, about_point=D), FadeIn(dot_E), FadeIn(label_E), run_time=2)
        
        line_DE = Line(D, E, color=GREEN)
        line_CE = Line(C, E, color=GREEN)
        self.play(Create(line_DE), Create(line_CE))
        
        self.wait_for_audio(2, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(label_D), FadeOut(line_CD),
                  FadeOut(dot_E), FadeOut(label_E), FadeOut(line_DE), FadeOut(line_CE), FadeOut(hint))
    
    def scene_3_proof(self):
        self.add_scene_audio(3)
        start_time = self.time
        self.show_layout("证明：∠ABE = 90°")
        
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
        
        proof = VGroup(
            Text("在△ACD 和△BED 中：", font_size=24),
            MathTex(r"CD = DE\ (\text{已知})", font_size=24),
            MathTex(r"\angle ADC = \angle BDE\ (\text{对顶角})", font_size=24),
            MathTex(r"\angle ACD = \angle BDE\ (\text{旋转})", font_size=24),
            MathTex(r"\therefore \triangle ACD \cong \triangle BED\ (SAS)", font_size=24),
            MathTex(r"\therefore \angle ABE = 90^\circ", font_size=24, color="#2ecc71")
        ).arrange(DOWN, buff=0.3)
        proof.move_to(self.FORMULA_CENTER)
        
        self.play(Write(proof))
        self.wait_for_audio(3, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(dot_E), FadeOut(line_BE),
                  FadeOut(triangle_ACD), FadeOut(triangle_BED), FadeOut(proof))
    
    def scene_4_q2(self):
        self.add_scene_audio(4)
        start_time = self.time
        self.show_layout("第 (2) 问：D 为 AB 中点")
        
        triangle, A, B, C = self.create_triangle_ABC(scale=0.5)
        D = Line(A, B).point_from_proportion(0.5)
        E = D + rotate_vector(C - D, PI/2)
        
        dot_D = Dot(D, color=YELLOW)
        label_D = Text("D（中点）", font_size=18, color=YELLOW).next_to(dot_D, UR)
        dot_E = Dot(E, color=GREEN)
        line_BE = Line(B, E, color=RED)
        
        self.add(triangle, dot_D, label_D, dot_E, line_BE)
        
        result = VGroup(
            MathTex(r"\text{由（1）：}\triangle ACD \cong \triangle BED", font_size=32),
            MathTex(r"\therefore BE = AC = 4", font_size=32, color="#2ecc71")
        ).arrange(DOWN, buff=0.5)
        result.move_to(self.FORMULA_CENTER)
        
        self.play(Write(result))
        self.wait_for_audio(4, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(label_D), FadeOut(dot_E),
                  FadeOut(line_BE), FadeOut(result))
    
    def scene_5_q2_calc(self):
        self.add_scene_audio(5)
        start_time = self.time
        self.show_layout("计算过程")
        
        placeholder = Text("图形辅助", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.DIAGRAM_CENTER)
        self.play(Write(placeholder))
        
        calc = VGroup(
            Text("步骤 1：求 AB", font_size=24),
            MathTex(r"AB^2 = AC^2 + BC^2 = 4^2 + 3^2 = 25", font_size=24),
            MathTex(r"\therefore AB = 5", font_size=24),
            Text("", font_size=24),
            Text("步骤 2：求 AD、BD", font_size=24),
            MathTex(r"D\text{是}AB\text{中点}", font_size=24),
            MathTex(r"\therefore AD = BD = 2.5", font_size=24),
            Text("", font_size=24),
            Text("步骤 3：求 BE", font_size=24),
            MathTex(r"\text{由（1）：}\triangle ACD \cong \triangle BED", font_size=24),
            MathTex(r"\therefore BE = AC = 4", font_size=24, color="#2ecc71")
        ).arrange(DOWN, buff=0.3)
        calc.move_to(self.FORMULA_CENTER)
        
        self.play(Write(calc))
        self.wait_for_audio(5, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(calc))
    
    def scene_6_q3_similar(self):
        self.add_scene_audio(6)
        start_time = self.time
        self.show_layout("第 (3) 问①：相似三角形")
        
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
        
        hint = VGroup(
            Text("关键：", font_size=28, color="#f39c12"),
            MathTex(r"\text{证明}\triangle ACD \sim \triangle CBD", font_size=28, color="#f39c12")
        ).arrange(DOWN, buff=0.5)
        hint.move_to(self.FORMULA_CENTER)
        
        self.play(Write(hint))
        self.wait_for_audio(6, self.time - start_time)
        self.play(FadeOut(triangle), FadeOut(dot_D), FadeOut(dot_E), FadeOut(line_CD),
                  FadeOut(line_DE), FadeOut(line_CE), FadeOut(triangle_ACD),
                  FadeOut(triangle_CBD), FadeOut(hint))
    
    def scene_7_q3_proof(self):
        self.add_scene_audio(7)
        start_time = self.time
        self.show_layout("证明：CE² = 2BD·AD")
        
        placeholder = Text("图形辅助", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.DIAGRAM_CENTER)
        self.play(Write(placeholder))
        
        proof = VGroup(
            Text("在 Rt△CDE 中：", font_size=24),
            MathTex(r"CE^2 = CD^2 + DE^2 = 2CD^2", font_size=24),
            Text("", font_size=24),
            Text("证明 CD² = BD·AD：", font_size=24),
            MathTex(r"\triangle ACD \sim \triangle CBD\ (\text{AA})", font_size=24),
            MathTex(r"\therefore \frac{AD}{CD} = \frac{CD}{BD}", font_size=24),
            MathTex(r"\text{即}CD^2 = BD \cdot AD", font_size=24),
            Text("", font_size=24),
            MathTex(r"\therefore CE^2 = 2CD^2 = 2BD \cdot AD", font_size=24, color="#2ecc71")
        ).arrange(DOWN, buff=0.3)
        proof.move_to(self.FORMULA_CENTER)
        
        self.play(Write(proof))
        self.wait_for_audio(7, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(proof))
    
    def scene_8_q3_minimum(self):
        self.add_scene_audio(8)
        start_time = self.time
        self.show_layout("求 CE 最小值")
        
        placeholder = Text("函数图像", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.DIAGRAM_CENTER)
        self.play(Write(placeholder))
        
        calc = VGroup(
            MathTex(r"\text{由①：}CE^2 = 2BD \cdot AD", font_size=24),
            MathTex(r"\text{设}AD = x\text{，则}BD = 5 - x", font_size=24),
            MathTex(r"CE^2 = 2(5-x)x = -2x^2 + 10x", font_size=24),
            Text("", font_size=24),
            Text("二次函数，开口向下，有最大值", font_size=24),
            MathTex(r"\text{当}x = 2.5\text{时，}CE^2_{max} = 12.5", font_size=24),
            Text("", font_size=24),
            MathTex(r"\therefore CE_{min} = \sqrt{12.5} = \frac{5\sqrt{2}}{2}", font_size=24, color="#2ecc71")
        ).arrange(DOWN, buff=0.3)
        calc.move_to(self.FORMULA_CENTER)
        
        self.play(Write(calc))
        self.wait_for_audio(8, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(calc))
    
    def scene_9_summary(self):
        self.add_scene_audio(9)
        start_time = self.time
        self.show_layout("答案汇总")
        
        placeholder = Text("回顾图形", font_size=24, color="#7f8c8d")
        placeholder.move_to(self.DIAGRAM_CENTER)
        self.play(Write(placeholder))
        
        summary = VGroup(
            Text("答案：", font_size=22),
            MathTex(r"(1)\ \triangle ACD \cong \triangle BED\ (SAS)\ \Rightarrow\ \angle ABE = 90^\circ", font_size=22),
            MathTex(r"(2)\ BE = 4", font_size=22),
            MathTex(r"(3)\text{①}\ CE^2 = 2BD \cdot AD", font_size=22),
            MathTex(r"\text{②}\ CE_{min} = \frac{5\sqrt{2}}{2}", font_size=22),
            Text("", font_size=22),
            Text("解题方法：", font_size=22),
            MathTex(r"1.\ \text{旋转全等}\ \rightarrow\ \text{证明垂直}", font_size=22),
            MathTex(r"2.\ \text{勾股定理}\ \rightarrow\ \text{求边长}", font_size=22),
            MathTex(r"3.\ \text{相似三角形}\ \rightarrow\ \text{建立关系}", font_size=22),
            MathTex(r"4.\ \text{二次函数}\ \rightarrow\ \text{求最值}", font_size=22),
            Text("", font_size=22),
            Text("谢谢观看！", font_size=32, color="#3498db")
        ).arrange(DOWN, buff=0.25)
        summary.move_to(self.FORMULA_CENTER)
        
        self.play(Write(summary))
        self.wait_for_audio(9, self.time - start_time)
        self.play(FadeOut(placeholder), FadeOut(summary),
                  FadeOut(self.title_box), FadeOut(self.diagram_box), FadeOut(self.formula_box))


if __name__ == "__main__":
    scene = GeometryRotationProblem()
    scene.render()
