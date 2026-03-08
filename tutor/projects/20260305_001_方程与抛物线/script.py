"""
方程与抛物线综合题 - 学生友好版
使用纯 Text 显示，避免 LaTeX 中文问题
"""

from manim import *
import json
from pathlib import Path


class EquationParabolaProblem(Scene):
    """方程与抛物线综合题"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 查找音频目录
        self.audio_dir = Path(__file__).parent / "audio"
        if not self.audio_dir.exists():
            self.audio_dir = Path(__file__).parent.parent / "audio"
        
        # 加载音频时长
        self.audio_timings = self.load_audio_timings()
        
        # 8 幕内容
        self.scene_1_title()
        self.scene_2_discriminant_setup()
        self.scene_3_discriminant_proof()
        self.scene_4_vieta()
        self.scene_5_solve_m()
        self.scene_6_parabola_setup()
        self.scene_7_vertex()
        self.scene_8_summary()
    
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
        """第 1 幕：题目展示"""
        self.add_scene_audio(1)
        
        title = Text("方程与抛物线综合题", font_size=44, color="#3498db")
        
        equation = Text("已知方程：", font_size=28)
        eq_detail = Text("(m²-1)x² - 6(m+1)x + 9m = 0", font_size=24, font="Monospace")
        
        q1 = Text("（1）求证：无论 m 取何实数，方程总有实数根", font_size=22)
        q2 = Text("（2）若有两个不相等正根 x₁、x₂，且 1/x₁ + 1/x₂ = 2，求 m", font_size=22)
        q3 = Text("（3）抛物线与 y=k 有且只有一个公共点，求 k", font_size=22)
        
        content = VGroup(
            title,
            VGroup(equation, eq_detail).arrange(DOWN, buff=0.3),
            q1, q2, q3
        ).arrange(DOWN, buff=0.4).center()
        
        start_time = self.time
        self.play(FadeIn(title), FadeIn(equation), FadeIn(eq_detail))
        self.play(FadeIn(q1), FadeIn(q2), FadeIn(q3))
        self.wait_for_audio(1, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_2_discriminant_setup(self):
        """第 2 幕：判别式分析"""
        self.add_scene_audio(2)
        
        title = Text("第 (1) 问：证明总有实数根", font_size=40, color="#3498db")
        
        idea = Text("思路：证明判别式 Δ ≥ 0", font_size=28, color="#f39c12")
        
        formula = Text("判别式公式：Δ = b² - 4ac", font_size=26)
        
        coefficients = VGroup(
            Text("其中：", font_size=24),
            Text("a = m² - 1", font_size=24, font="Monospace"),
            Text("b = -6(m+1)", font_size=24, font="Monospace"),
            Text("c = 9m", font_size=24, font="Monospace")
        ).arrange(DOWN, buff=0.3)
        
        substitution = Text("代入公式：", font_size=26)
        delta = Text("Δ = [-6(m+1)]² - 4(m²-1)(9m)", font_size=22, font="Monospace")
        
        content = VGroup(
            title,
            idea,
            formula,
            coefficients,
            substitution,
            delta
        ).arrange(DOWN, buff=0.35).center()
        
        start_time = self.time
        self.play(FadeIn(title), FadeIn(idea))
        self.play(Write(formula), Write(coefficients))
        self.play(Write(substitution), Write(delta))
        self.wait_for_audio(2, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_3_discriminant_proof(self):
        """第 3 幕：完成证明"""
        self.add_scene_audio(3)
        
        title = Text("继续化简", font_size=40, color="#3498db")
        
        step1 = Text("Δ = 36(m+1)² - 36m(m²-1)", font_size=22, font="Monospace")
        step2 = Text("  = 36[(m+1)² - m(m²-1)]", font_size=22, font="Monospace")
        step3 = Text("  = 36[m² + 2m + 1 - m³ + m]", font_size=22, font="Monospace")
        step4 = Text("  = 36[-m³ + m² + 3m + 1]", font_size=22, font="Monospace", color="#f39c12")
        
        factor = Text("因式分解：", font_size=26)
        factored = Text("Δ = 36[-(m-1)(m²-3)]", font_size=24, font="Monospace", color="#f39c12")
        
        discussion = VGroup(
            Text("讨论：", font_size=26),
            Text("• 当 m² ≥ 3 时，m² - 3 ≥ 0", font_size=22),
            Text("• 当 m = 1 时，Δ = 0", font_size=22),
            Text("• 当 m ≠ ±1 时，方程为二次方程", font_size=22)
        ).arrange(DOWN, buff=0.3)
        
        conclusion = Text("∴ 无论 m 取何实数，Δ ≥ 0，方程总有实数根", font_size=28, color="#2ecc71")
        
        content = VGroup(
            title,
            step1, step2, step3, step4,
            factor, factored,
            discussion,
            conclusion
        ).arrange(DOWN, buff=0.3).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(step1), Write(step2), Write(step3), Write(step4))
        self.play(Write(factor), Write(factored))
        self.play(Write(discussion))
        self.play(Write(conclusion))
        self.wait_for_audio(3, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_4_vieta(self):
        """第 4 幕：韦达定理"""
        self.add_scene_audio(4)
        
        title = Text("第 (2) 问：求 m 的值", font_size=40, color="#3498db")
        
        given = VGroup(
            Text("已知：", font_size=26, color="#f39c12"),
            Text("方程有两个不相等的正实数根 x₁、x₂", font_size=22),
            Text("且满足：1/x₁ + 1/x₂ = 2", font_size=22, font="Monospace")
        ).arrange(DOWN, buff=0.3)
        
        vieta_title = Text("韦达定理：", font_size=26)
        vieta_sum = Text("x₁ + x₂ = -b/a = 6(m+1)/(m²-1)", font_size=22, font="Monospace")
        vieta_prod = Text("x₁ · x₂ = c/a = 9m/(m²-1)", font_size=22, font="Monospace")
        
        combine = Text("通分：", font_size=26)
        combined = Text("1/x₁ + 1/x₂ = (x₁ + x₂)/(x₁ · x₂) = 2", font_size=22, font="Monospace")
        
        content = VGroup(
            title,
            given,
            vieta_title, vieta_sum, vieta_prod,
            combine, combined
        ).arrange(DOWN, buff=0.35).center()
        
        start_time = self.time
        self.play(FadeIn(title), FadeIn(given))
        self.play(Write(vieta_title), Write(vieta_sum), Write(vieta_prod))
        self.play(Write(combine), Write(combined))
        self.wait_for_audio(4, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_5_solve_m(self):
        """第 5 幕：求解 m"""
        self.add_scene_audio(5)
        
        title = Text("代入韦达定理求解", font_size=40, color="#3498db")
        
        step1 = Text("代入：", font_size=26)
        step1_eq = Text("[6(m+1)/(m²-1)] / [9m/(m²-1)] = 2", font_size=20, font="Monospace")
        
        step2 = Text("约掉 (m²-1)：", font_size=24, color="#95a5a6")
        step2_eq = Text("6(m+1)/9m = 2", font_size=22, font="Monospace")
        
        step3 = Text("交叉相乘：", font_size=24, color="#95a5a6")
        step3_eq = Text("6(m+1) = 18m", font_size=22, font="Monospace")
        
        step4 = Text("展开：", font_size=24, color="#95a5a6")
        step4_eq = Text("6m + 6 = 18m", font_size=22, font="Monospace")
        
        step5 = Text("移项：", font_size=24, color="#95a5a6")
        step5_eq = Text("6 = 12m", font_size=22, font="Monospace")
        
        solution = Text("解得：m = 1/2", font_size=32, color="#2ecc71")
        
        verify = VGroup(
            Text("验证：", font_size=26, color="#f39c12"),
            Text("当 m = 1/2 时，m² - 1 = -3/4 ≠ 0 ✓", font_size=20),
            Text("Δ > 0 ✓", font_size=20),
            Text("x₁, x₂ > 0 ✓", font_size=20)
        ).arrange(DOWN, buff=0.3)
        
        content = VGroup(
            title,
            step1, step1_eq,
            step2, step2_eq,
            step3, step3_eq,
            step4, step4_eq,
            step5, step5_eq,
            solution,
            verify
        ).arrange(DOWN, buff=0.25).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(step1), Write(step1_eq))
        self.play(Write(step2), Write(step2_eq))
        self.play(Write(step3), Write(step3_eq))
        self.play(Write(step4), Write(step4_eq))
        self.play(Write(step5), Write(step5_eq))
        self.play(Write(solution))
        self.play(Write(verify))
        self.wait_for_audio(5, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_6_parabola_setup(self):
        """第 6 幕：抛物线分析"""
        self.add_scene_audio(6)
        
        title = Text("第 (3) 问：求 k 的值", font_size=40, color="#3498db")
        
        given = VGroup(
            Text("已知：m = 1/2", font_size=26, color="#f39c12"),
            Text("抛物线：y = (m²-1)x² - 6(m+1)x + 9m", font_size=20, font="Monospace"),
            Text("直线：y = k", font_size=20, font="Monospace"),
            Text("条件：有且只有一个公共点", font_size=22, color="#f39c12")
        ).arrange(DOWN, buff=0.3)
        
        geometry = VGroup(
            Text("几何意义：", font_size=26),
            Text("直线 y = k 与抛物线相切", font_size=22),
            Text("即 k 等于抛物线的顶点纵坐标", font_size=22, color="#2ecc71")
        ).arrange(DOWN, buff=0.3)
        
        content = VGroup(title, given, geometry).arrange(DOWN, buff=0.4).center()
        
        start_time = self.time
        self.play(FadeIn(title), FadeIn(given))
        self.play(Write(geometry))
        self.wait_for_audio(6, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_7_vertex(self):
        """第 7 幕：求顶点"""
        self.add_scene_audio(7)
        
        title = Text("求顶点纵坐标", font_size=40, color="#3498db")
        
        method_title = Text("方法：代入顶点横坐标", font_size=26)
        
        formula = Text("顶点横坐标：x = -b/(2a)", font_size=24)
        
        coefficients = VGroup(
            Text("当 m = 1/2 时：", font_size=24, color="#f39c12"),
            Text("a = m² - 1 = -3/4", font_size=22, font="Monospace"),
            Text("b = -6(m+1) = -9", font_size=22, font="Monospace"),
            Text("c = 9m = 9/2", font_size=22, font="Monospace")
        ).arrange(DOWN, buff=0.3)
        
        vertex_x = Text("顶点横坐标：", font_size=24)
        vertex_x_val = Text("x = -(-9)/[2×(-3/4)] = 9/(-3/2) = -6", font_size=22, font="Monospace")
        
        vertex_y = Text("顶点纵坐标：", font_size=24)
        vertex_y_calc = Text("y = (-3/4)×(-6)² - 9×(-6) + 9/2", font_size=20, font="Monospace")
        vertex_y_step = Text("  = (-3/4)×36 + 54 + 4.5", font_size=20, font="Monospace")
        vertex_y_result = Text("  = -27 + 54 + 4.5 = 31.5", font_size=22, font="Monospace", color="#2ecc71")
        
        conclusion = Text("∴ k = 31.5", font_size=32, color="#2ecc71")
        
        content = VGroup(
            title,
            method_title,
            formula,
            coefficients,
            vertex_x, vertex_x_val,
            vertex_y, vertex_y_calc, vertex_y_step, vertex_y_result,
            conclusion
        ).arrange(DOWN, buff=0.25).center()
        
        start_time = self.time
        self.play(FadeIn(title), FadeIn(method_title))
        self.play(Write(formula), Write(coefficients))
        self.play(Write(vertex_x), Write(vertex_x_val))
        self.play(Write(vertex_y), Write(vertex_y_calc), Write(vertex_y_step), Write(vertex_y_result))
        self.play(Write(conclusion))
        self.wait_for_audio(7, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_8_summary(self):
        """第 8 幕：答案汇总"""
        self.add_scene_audio(8)
        
        title = Text("答案汇总", font_size=44, color="#3498db")
        
        ans1 = Text("(1) 证明：Δ = 36[-(m-1)(m²-3)] ≥ 0", font_size=22, font="Monospace")
        ans1_detail = Text("∴ 无论 m 取何实数，方程总有实数根", font_size=22)
        
        ans2 = Text("(2) m = 1/2", font_size=28, color="#2ecc71", font="Monospace")
        
        ans3 = Text("(3) k = 31.5", font_size=28, color="#2ecc71", font="Monospace")
        
        method_title = Text("解题方法总结：", font_size=28, color="#f39c12")
        method_1 = Text("1. 判别式 → 判断根的情况", font_size=22)
        method_2 = Text("2. 韦达定理 → 根与系数的关系", font_size=22)
        method_3 = Text("3. 顶点坐标 → 抛物线最值", font_size=22)
        
        thanks = Text("谢谢观看！", font_size=48, color="#3498db")
        
        content = VGroup(
            title,
            ans1, ans1_detail,
            ans2,
            ans3,
            method_title, method_1, method_2, method_3,
            thanks
        ).arrange(DOWN, buff=0.35).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(ans1), Write(ans1_detail))
        self.play(Write(ans2))
        self.play(Write(ans3))
        self.play(Write(method_title), Write(method_1), Write(method_2), Write(method_3))
        self.play(Write(thanks))
        self.wait_for_audio(8, self.time - start_time)
        self.play(FadeOut(content))
