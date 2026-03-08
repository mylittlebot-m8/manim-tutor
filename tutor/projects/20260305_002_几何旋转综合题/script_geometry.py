"""
几何旋转综合题 - 动态几何图形版
包含：动态画图、旋转动画、标注显示
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
    """几何旋转综合题 - 动态图形版"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 查找音频目录
        self.audio_dir = Path(__file__).parent / "audio"
        if not self.audio_dir.exists():
            self.audio_dir = Path(__file__).parent.parent / "audio"
        
        # 加载音频时长
        self.audio_timings = self.load_audio_timings()
        
        # 9 幕内容（带动态图形）
        self.scene_1_draw_figure()
        self.scene_2_rotation_demo()
        self.scene_3_proof_animation()
        self.scene_4_q2_midpoint()
        self.scene_5_q2_calculate()
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
    
    def create_triangle_ABC(self):
        """创建 Rt△ABC"""
        # 定义点（按比例）
        C = ORIGIN
        B = RIGHT * 3  # BC = 3
        A = UP * 4     # AC = 4
        
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
        right_angle = RightAngle(line_AC, line_BC, length=0.4, color=RED)
        
        # 边长标注
        label_AC = Text("4", font_size=20, color=GREEN).next_to(Line(A, C), LEFT)
        label_BC = Text("3", font_size=20, color=GREEN).next_to(Line(B, C), DOWN)
        
        return VGroup(
            triangle,
            dot_A, dot_B, dot_C,
            label_A, label_B, label_C,
            right_angle,
            label_AC, label_BC
        ), A, B, C
    
    def scene_1_draw_figure(self):
        """第 1 幕：绘制几何图形"""
        self.add_scene_audio(1)
        
        title = Text("几何旋转综合题", font_size=48, color="#3498db")
        title.to_edge(UP)
        
        # 逐步绘制图形
        triangle, A, B, C = self.create_triangle_ABC()
        
        # 动画：逐步显示
        start_time = self.time
        self.play(Write(title))
        self.play(Create(triangle[0]))  # 三角形
        self.play(FadeIn(triangle[1:4]))  # 点
        self.play(FadeIn(triangle[4:7]))  # 标签
        self.play(Create(triangle[7]))  # 直角标记
        self.play(FadeIn(triangle[8:10]))  # 边长
        
        # 显示题目文字
        problem = Tex(r"在 Rt$\triangle ABC$ 中，$\angle ACB = 90^\circ$，$AC = 4$，$BC = 3$", 
                     font_size=28).to_edge(DOWN)
        self.play(Write(problem))
        
        self.wait_for_audio(1, self.time - start_time)
        self.play(FadeOut(title), FadeOut(triangle), FadeOut(problem))
    
    def scene_2_rotation_demo(self):
        """第 2 幕：旋转动画演示"""
        self.add_scene_audio(2)
        
        title = Text("第 (1) 问：求证 ∠ABE = 90°", font_size=40, color="#3498db")
        title.to_edge(UP)
        
        # 创建基础图形
        triangle, A, B, C = self.create_triangle_ABC()
        self.add(triangle)
        
        # 创建点 D（AB 上任意一点）
        D = Line(A, B).point_from_proportion(0.6)
        dot_D = Dot(D, color=YELLOW)
        label_D = Text("D", font_size=24, color=YELLOW).next_to(dot_D, UR)
        
        # 创建 CD
        line_CD = Line(C, D, color=YELLOW)
        
        # 创建旋转后的三角形 CDE
        # 将 CD 绕 D 逆时针旋转 90° 得到 DE
        E = D + rotate_vector(C - D, PI/2)
        dot_E = Dot(E, color=GREEN)
        label_E = Text("E", font_size=24, color=GREEN).next_to(dot_E, DL)
        
        line_DE = Line(D, E, color=GREEN)
        line_CE = Line(C, E, color=GREEN)
        triangle_CDE = Polygon(C, D, E, color=GREEN, fill_opacity=0.3)
        
        # 直角标记
        right_angle_D = RightAngle(line_CD, line_DE, length=0.3, color=RED)
        
        # 动画演示
        start_time = self.time
        self.play(FadeIn(dot_D), FadeIn(label_D))
        self.play(Create(line_CD))
        
        # 旋转动画
        self.play(
            Rotate(line_CD, PI/2, about_point=D),
            FadeIn(dot_E),
            FadeIn(label_E),
            run_time=2
        )
        
        self.play(Create(line_DE), Create(line_CE))
        self.play(Create(triangle_CDE))
        self.play(Create(right_angle_D))
        
        # 显示关键提示
        hint = Tex(r"$\triangle CDE$ 可看作 $\triangle CDB$ 绕点 $D$ 旋转 90° 得到", 
                  font_size=24, color="#f39c12").to_edge(DOWN)
        self.play(Write(hint))
        
        self.wait_for_audio(2, self.time - start_time)
        self.play(FadeOut(title), FadeOut(triangle), FadeOut(dot_D), FadeOut(label_D),
                  FadeOut(line_CD), FadeOut(dot_E), FadeOut(label_E),
                  FadeOut(line_DE), FadeOut(line_CE), FadeOut(triangle_CDE),
                  FadeOut(right_angle_D), FadeOut(hint))
    
    def scene_3_proof_animation(self):
        """第 3 幕：证明动画"""
        self.add_scene_audio(3)
        
        title = Text("证明：", font_size=44, color="#3498db")
        title.to_edge(UP)
        
        # 创建完整的几何图形
        triangle, A, B, C = self.create_triangle_ABC()
        self.add(triangle)
        
        D = Line(A, B).point_from_proportion(0.6)
        E = D + rotate_vector(C - D, PI/2)
        
        # 连接线
        line_AD = Line(A, D, color=BLUE)
        line_BD = Line(B, D, color=BLUE)
        line_CD = Line(C, D, color=YELLOW)
        line_DE = Line(D, E, color=GREEN)
        line_BE = Line(B, E, color=RED)
        
        # 高亮两个三角形
        triangle_ACD = Polygon(A, C, D, color=BLUE, fill_opacity=0.4)
        triangle_BED = Polygon(B, E, D, color=GREEN, fill_opacity=0.4)
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Create(line_AD), Create(line_BD))
        self.play(Create(line_CD), Create(line_DE), Create(line_BE))
        
        # 高亮全等三角形
        self.play(FadeIn(triangle_ACD), FadeIn(triangle_BED))
        
        # 显示证明步骤
        step1 = Tex(r"在 $\triangle ACD$ 和 $\triangle BED$ 中：", 
                   font_size=26).to_edge(DOWN)
        step2 = Tex(r"$CD = DE$（已知）", font_size=24).next_to(step1, DOWN)
        step3 = Tex(r"$\angle ADC = \angle BDE$（对顶角）", font_size=24).next_to(step2, DOWN)
        step4 = Tex(r"$\angle ACD = \angle BDE$（旋转）", font_size=24).next_to(step3, DOWN)
        
        self.play(Write(step1))
        self.play(Write(step2))
        self.play(Write(step3))
        self.play(Write(step4))
        
        congruent = Tex(r"$\therefore \triangle ACD \cong \triangle BED$（SAS）", 
                       font_size=26, color="#f39c12").next_to(step4, DOWN)
        self.play(Write(congruent))
        
        final = Tex(r"$\therefore \angle ABE = 90^\circ$  得证", 
                   font_size=28, color="#2ecc71").next_to(congruent, DOWN)
        self.play(Write(final))
        
        self.wait_for_audio(3, self.time - start_time)
        self.play(FadeOut(title), FadeOut(triangle), FadeOut(line_AD), FadeOut(line_BD),
                  FadeOut(line_CD), FadeOut(line_DE), FadeOut(line_BE),
                  FadeOut(triangle_ACD), FadeOut(triangle_BED),
                  FadeOut(step1), FadeOut(step2), FadeOut(step3), FadeOut(step4),
                  FadeOut(congruent), FadeOut(final))
    
    def scene_4_q2_midpoint(self):
        """第 4 幕：第 2 问 - 中点"""
        self.add_scene_audio(4)
        
        title = Text("第 (2) 问：当 D 为 AB 中点时，求 BE 的长", font_size=36, color="#3498db")
        title.to_edge(UP)
        
        # 创建图形（D 为中点）
        triangle, A, B, C = self.create_triangle_ABC()
        self.add(triangle)
        
        D = Line(A, B).point_from_proportion(0.5)  # 中点
        E = D + rotate_vector(C - D, PI/2)
        
        dot_D = Dot(D, color=YELLOW)
        label_D = Text("D（中点）", font_size=20, color=YELLOW).next_to(dot_D, UR)
        
        line_BE = Line(B, E, color=RED)
        dot_E = Dot(E, color=GREEN)
        label_E = Text("E", font_size=24, color=GREEN).next_to(dot_E, DL)
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        self.play(FadeIn(dot_D), FadeIn(label_D))
        self.play(Create(line_BE), FadeIn(dot_E), FadeIn(label_E))
        
        # 显示提示
        hint = Tex(r"由（1）知：$\triangle ACD \cong \triangle BED$", 
                  font_size=26, color="#f39c12").to_edge(DOWN)
        self.play(Write(hint))
        
        result = Tex(r"$\therefore BE = AC = 4$", font_size=32, color="#2ecc71").next_to(hint, DOWN)
        self.play(Write(result))
        
        self.wait_for_audio(4, self.time - start_time)
        self.play(FadeOut(title), FadeOut(triangle), FadeOut(dot_D), FadeOut(label_D),
                  FadeOut(line_BE), FadeOut(dot_E), FadeOut(label_E),
                  FadeOut(hint), FadeOut(result))
    
    def scene_5_q2_calculate(self):
        """第 5 幕：第 2 问 - 计算过程"""
        self.add_scene_audio(5)
        
        title = Text("解：", font_size=44, color="#3498db")
        title.to_edge(UP)
        
        # 逐步显示计算步骤
        step1_title = Text("步骤 1：求 AB 的长", font_size=28, color="#3498db")
        pythagoras = Tex(r"在 Rt$\triangle ABC$ 中，由勾股定理：", font_size=24)
        calc1 = Tex(r"$AB^2 = AC^2 + BC^2 = 4^2 + 3^2 = 16 + 9 = 25$", font_size=24)
        result1 = Tex(r"$\therefore AB = 5$", font_size=26)
        
        step2_title = Text("步骤 2：求 AD、BD 的长", font_size=28, color="#3498db")
        midpoint = Tex(r"$\because D$ 是 $AB$ 中点", font_size=24)
        result2 = Tex(r"$\therefore AD = BD = \frac{AB}{2} = 2.5$", font_size=24)
        
        step3_title = Text("步骤 3：求 BE 的长", font_size=28, color="#3498db")
        congruent = Tex(r"由（1）知：$\triangle ACD \cong \triangle BED$", font_size=24)
        final = Tex(r"$\therefore BE = AC = 4$", font_size=28, color="#2ecc71")
        
        answer = Tex(r"答：$BE = 4$", font_size=32, color="#2ecc71")
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        
        self.play(Write(step1_title), Write(pythagoras), Write(calc1), Write(result1))
        self.play(Write(step2_title), Write(midpoint), Write(result2))
        self.play(Write(step3_title), Write(congruent), Write(final))
        self.play(Write(answer))
        
        self.wait_for_audio(5, self.time - start_time)
        self.play(FadeOut(title), FadeOut(step1_title), FadeOut(pythagoras), 
                  FadeOut(calc1), FadeOut(result1), FadeOut(step2_title),
                  FadeOut(midpoint), FadeOut(result2), FadeOut(step3_title),
                  FadeOut(congruent), FadeOut(final), FadeOut(answer))
    
    def scene_6_q3_similar(self):
        """第 6 幕：第 3 问① - 相似三角形"""
        self.add_scene_audio(6)
        
        title = Tex(r"第 (3) 问①：求证 $CE^2 = 2BD \cdot AD$", font_size=36)
        title.to_edge(UP)
        
        # 创建图形
        triangle, A, B, C = self.create_triangle_ABC()
        self.add(triangle)
        
        D = Line(A, B).point_from_proportion(0.6)
        E = D + rotate_vector(C - D, PI/2)
        
        dot_D = Dot(D, color=YELLOW)
        label_D = Text("D", font_size=24, color=YELLOW).next_to(dot_D, UR)
        dot_E = Dot(E, color=GREEN)
        label_E = Text("E", font_size=24, color=GREEN).next_to(dot_E, DL)
        
        line_CD = Line(C, D, color=YELLOW)
        line_DE = Line(D, E, color=GREEN)
        line_CE = Line(C, E, color=GREEN)
        
        # 高亮相似三角形
        triangle_ACD = Polygon(A, C, D, color=BLUE, fill_opacity=0.3)
        triangle_CBD = Polygon(C, B, D, color=RED, fill_opacity=0.3)
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        self.play(FadeIn(dot_D), FadeIn(label_D), FadeIn(dot_E), FadeIn(label_E))
        self.play(Create(line_CD), Create(line_DE), Create(line_CE))
        
        # 高亮相似三角形
        self.play(FadeIn(triangle_ACD), FadeIn(triangle_CBD))
        
        # 显示思路
        idea = Tex(r"关键：证明 $\triangle ACD \sim \triangle CBD$", 
                  font_size=26, color="#f39c12").to_edge(DOWN)
        self.play(Write(idea))
        
        self.wait_for_audio(6, self.time - start_time)
        self.play(FadeOut(title), FadeOut(triangle), FadeOut(dot_D), FadeOut(label_D),
                  FadeOut(dot_E), FadeOut(label_E), FadeOut(line_CD), FadeOut(line_DE),
                  FadeOut(line_CE), FadeOut(triangle_ACD), FadeOut(triangle_CBD),
                  FadeOut(idea))
    
    def scene_7_q3_proof(self):
        """第 7 幕：第 3 问① - 证明"""
        self.add_scene_audio(7)
        
        title = Text("证明：", font_size=44, color="#3498db")
        title.to_edge(UP)
        
        # 逐步显示证明
        step1 = Tex(r"在 Rt$\triangle CDE$ 中：", font_size=26)
        pythagoras = Tex(r"$CE^2 = CD^2 + DE^2$（勾股定理）", font_size=24)
        equal = Tex(r"$= CD^2 + CD^2$（$\because CD = DE$）", font_size=24)
        result1 = Tex(r"$= 2CD^2$", font_size=24)
        
        step2 = Tex(r"证明 $CD^2 = BD \cdot AD$：", font_size=26)
        similar = Tex(r"在 $\triangle ACD$ 和 $\triangle CBD$ 中：", font_size=24)
        angle1 = Tex(r"$\angle A = \angle BCD$（同角的余角相等）", font_size=24)
        angle2 = Tex(r"$\angle ADC = \angle CDB$（公共角）", font_size=24)
        congruent = Tex(r"$\therefore \triangle ACD \sim \triangle CBD$（AA）", font_size=24)
        ratio = Tex(r"$\therefore \frac{AD}{CD} = \frac{CD}{BD}$", font_size=24)
        result2 = Tex(r"即 $CD^2 = BD \cdot AD$", font_size=24)
        
        final = Tex(r"$\therefore CE^2 = 2CD^2 = 2BD \cdot AD$  得证", 
                   font_size=28, color="#2ecc71")
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        
        self.play(Write(step1), Write(pythagoras), Write(equal), Write(result1))
        self.play(Write(step2), Write(similar))
        self.play(Write(angle1), Write(angle2))
        self.play(Write(congruent), Write(ratio), Write(result2))
        self.play(Write(final))
        
        self.wait_for_audio(7, self.time - start_time)
        self.play(FadeOut(title), FadeOut(step1), FadeOut(pythagoras), FadeOut(equal),
                  FadeOut(result1), FadeOut(step2), FadeOut(similar), FadeOut(angle1),
                  FadeOut(angle2), FadeOut(congruent), FadeOut(ratio), FadeOut(result2),
                  FadeOut(final))
    
    def scene_8_q3_minimum(self):
        """第 8 幕：第 3 问② - 求最小值"""
        self.add_scene_audio(8)
        
        title = Tex(r"第 (3) 问②：求 $CE$ 的最小值", font_size=36)
        title.to_edge(UP)
        
        # 显示函数推导
        step1 = Tex(r"由①知：$CE^2 = 2BD \cdot AD$", font_size=26)
        
        step2 = Tex(r"设 $AD = x$，则 $BD = 5 - x$（$\because AB = 5$）", font_size=24)
        
        function = Tex(r"$CE^2 = 2(5-x) \cdot x = -2x^2 + 10x$", font_size=24)
        
        analysis = Tex(r"这是关于 $x$ 的二次函数，开口向下，有最大值", font_size=24)
        
        vertex = Tex(r"当 $x = -\frac{b}{2a} = \frac{10}{4} = 2.5$ 时", font_size=24)
        
        max_val = Tex(r"$CE^2$ 最大值 $= -2(2.5)^2 + 10(2.5) = 12.5$", font_size=24)
        
        final = Tex(r"$\therefore CE$ 最小值 $= \sqrt{12.5} = \frac{5\sqrt{2}}{2}$", 
                   font_size=28, color="#2ecc71")
        
        note = Tex(r"此时 $D$ 为 $AB$ 中点", font_size=24)
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        
        self.play(Write(step1), Write(step2))
        self.play(Write(function))
        self.play(Write(analysis))
        self.play(Write(vertex), Write(max_val))
        self.play(Write(final), Write(note))
        
        self.wait_for_audio(8, self.time - start_time)
        self.play(FadeOut(title), FadeOut(step1), FadeOut(step2), FadeOut(function),
                  FadeOut(analysis), FadeOut(vertex), FadeOut(max_val),
                  FadeOut(final), FadeOut(note))
    
    def scene_9_summary(self):
        """第 9 幕：答案汇总"""
        self.add_scene_audio(9)
        
        title = Text("答案汇总", font_size=48, color="#3498db")
        title.to_edge(UP)
        
        ans1 = Tex(r"(1) 证明：$\triangle ACD \cong \triangle BED$（SAS）", font_size=24)
        ans1_result = Tex(r"$\therefore \angle ABE = 90^\circ$", font_size=24)
        
        ans2 = Tex(r"(2) $BE = 4$", font_size=28, color="#2ecc71")
        
        ans3_1 = Tex(r"(3) ① 证明：$CE^2 = 2BD \cdot AD$", font_size=24)
        ans3_2 = Tex(r"② $CE$ 最小值 $= \frac{5\sqrt{2}}{2}$", font_size=28, color="#2ecc71")
        
        method_title = Text("解题方法总结：", font_size=28, color="#f39c12")
        method1 = Text("1. 旋转全等 → 证明垂直", font_size=22)
        method2 = Text("2. 勾股定理 → 求边长", font_size=22)
        method3 = Text("3. 相似三角形 → 建立关系", font_size=22)
        method4 = Text("4. 二次函数 → 求最值", font_size=22)
        
        thanks = Text("谢谢观看！", font_size=48, color="#3498db")
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        
        self.play(Write(ans1), Write(ans1_result))
        self.play(Write(ans2))
        self.play(Write(ans3_1), Write(ans3_2))
        
        self.play(Write(method_title), Write(method1), Write(method2), 
                  Write(method3), Write(method4))
        self.play(Write(thanks))
        
        self.wait_for_audio(9, self.time - start_time)
        self.play(FadeOut(title), FadeOut(ans1), FadeOut(ans1_result),
                  FadeOut(ans2), FadeOut(ans3_1), FadeOut(ans3_2),
                  FadeOut(method_title), FadeOut(method1), FadeOut(method2),
                  FadeOut(method3), FadeOut(method4), FadeOut(thanks))


if __name__ == "__main__":
    scene = GeometryRotationProblem()
    scene.render()
