"""
几何旋转综合题 - 使用 xelatex 支持中文
"""

from manim import *
import json
from pathlib import Path

# ========== 关键配置：使用 xelatex 支持中文 ==========
config.tex_compiler = "xelatex"

# 创建全局支持中文的 TexTemplate
template = TexTemplate()
template.tex_compiler = "xelatex"
template.output_format = ".xdv"
template.add_to_preamble(r"\usepackage{xeCJK}")
template.add_to_preamble(r"\setCJKmainfont{WenQuanYi Zen Hei}")

# 设置全局模板
config.tex_template = template
# ==================================================


class GeometryRotationProblem(Scene):
    """几何旋转综合题"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 查找音频目录
        self.audio_dir = Path(__file__).parent / "audio"
        if not self.audio_dir.exists():
            self.audio_dir = Path(__file__).parent.parent / "audio"
        
        # 加载音频时长
        self.audio_timings = self.load_audio_timings()
        
        # 9 幕内容
        self.scene_1_title()
        self.scene_2_analysis()
        self.scene_3_proof()
        self.scene_4_q2_setup()
        self.scene_5_q2_solve()
        self.scene_6_q3_1_setup()
        self.scene_7_q3_1_proof()
        self.scene_8_q3_2_solve()
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
    
    def scene_1_title(self):
        """第 1 幕：题目展示"""
        self.add_scene_audio(1)
        
        title = Text("几何旋转综合题", font_size=48, color="#3498db")
        
        # 使用 Tex 支持中文 + 公式（全局已配置 xelatex）
        given = Tex(r"在 Rt$\triangle ABC$ 中，$\angle ACB = 90^\circ$，$AC = 4$，$BC = 3$", 
                   font_size=28)
        
        condition = Tex(r"点 $D$ 是斜边 $AB$ 上一动点", font_size=26)
        construction = Tex(r"作 $\triangle CDE$，使得 $\angle CDE = 90^\circ$，$CD = DE$", 
                          font_size=26)
        
        q1 = Tex(r"(1) 求证：$\angle ABE = 90^\circ$", font_size=24, color="#2ecc71")
        q2 = Tex(r"(2) 当 $D$ 为 $AB$ 中点时，求 $BE$ 的长", font_size=24, color="#2ecc71")
        q3 = Tex(r"(3) ① 求证：$CE^2 = 2BD \cdot AD$；② 求 $CE$ 的最小值", 
                font_size=24, color="#2ecc71")
        
        content = VGroup(
            title,
            given,
            condition,
            construction,
            q1, q2, q3
        ).arrange(DOWN, buff=0.35).center()
        
        start_time = self.time
        self.play(FadeIn(title), FadeIn(given))
        self.play(Write(condition), Write(construction))
        self.play(Write(q1), Write(q2), Write(q3))
        self.wait_for_audio(1, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_2_analysis(self):
        """第 2 幕：第 1 问分析"""
        self.add_scene_audio(2)
        
        title = Text("第 (1) 问：求证 ∠ABE = 90°", font_size=40, color="#3498db")
        
        known = Tex(r"已知：$\angle ACB = 90^\circ$，$\angle CDE = 90^\circ$，$CD = DE$")
        
        idea = Tex(r"思路：$\triangle CDE$ 可看作 $\triangle CDB$ 绕点 $D$ 旋转 90° 得到", 
                  font_size=24, color="#f39c12")
        
        key = Tex(r"关键：证明 $\triangle ACD \cong \triangle BED$", 
                 font_size=26, color="#2ecc71")
        
        content = VGroup(title, known, idea, key).arrange(DOWN, buff=0.4).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(known), Write(idea))
        self.play(Write(key))
        self.wait_for_audio(2, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_3_proof(self):
        """第 3 幕：完成证明"""
        self.add_scene_audio(3)
        
        title = Text("证明：", font_size=44, color="#3498db")
        
        step1 = Tex(r"在 $\triangle ACD$ 和 $\triangle BED$ 中：", font_size=26)
        
        conditions = VGroup(
            Tex(r"$CD = DE$（已知）"),
            Tex(r"$\angle ADC = \angle BDE$（对顶角相等）"),
            Tex(r"$\angle ACD = \angle BDE$（旋转）")
        ).arrange(DOWN, buff=0.3)
        
        congruent = Tex(r"$\therefore \triangle ACD \cong \triangle BED$（SAS）", 
                       font_size=26, color="#f39c12")
        
        angle = Tex(r"$\therefore \angle CAD = \angle EBD$")
        
        final = Tex(r"$\because \angle CAD + \angle CBA = 90^\circ$")
        final2 = Tex(r"$\therefore \angle EBD + \angle CBA = 90^\circ$")
        conclusion = Tex(r"即 $\angle ABE = 90^\circ$  得证", font_size=28, color="#2ecc71")
        
        content = VGroup(
            title,
            step1,
            conditions,
            congruent,
            angle,
            final,
            final2,
            conclusion
        ).arrange(DOWN, buff=0.25).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(step1), Write(conditions))
        self.play(Write(congruent))
        self.play(Write(angle))
        self.play(Write(final), Write(final2))
        self.play(Write(conclusion))
        self.wait_for_audio(3, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_4_q2_setup(self):
        """第 4 幕：第 2 问分析"""
        self.add_scene_audio(4)
        
        title = Text("第 (2) 问：当 D 为 AB 中点时，求 BE 的长", font_size=36, color="#3498db")
        
        known = Tex(r"已知：$AC = 4$，$BC = 3$，$D$ 是 $AB$ 中点")
        
        idea = Tex(r"思路：利用（1）的全等结论：$BE = AC$", font_size=26, color="#f39c12")
        
        content = VGroup(title, known, idea).arrange(DOWN, buff=0.4).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(known))
        self.play(Write(idea))
        self.wait_for_audio(4, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_5_q2_solve(self):
        """第 5 幕：第 2 问求解"""
        self.add_scene_audio(5)
        
        title = Text("解：", font_size=44, color="#3498db")
        
        step1 = Tex(r"步骤 1：求 $AB$ 的长", font_size=28, color="#3498db")
        pythagoras = Tex(r"在 Rt$\triangle ABC$ 中，由勾股定理：")
        calc1 = Tex(r"$AB^2 = AC^2 + BC^2 = 4^2 + 3^2 = 16 + 9 = 25$")
        result1 = Tex(r"$\therefore AB = 5$")
        
        step2 = Tex(r"步骤 2：求 $AD$、$BD$ 的长", font_size=28, color="#3498db")
        midpoint = Tex(r"$\because D$ 是 $AB$ 中点")
        result2 = Tex(r"$\therefore AD = BD = \frac{AB}{2} = 2.5$")
        
        step3 = Tex(r"步骤 3：求 $BE$ 的长", font_size=28, color="#3498db")
        congruent2 = Tex(r"由（1）知：$\triangle ACD \cong \triangle BED$")
        final = Tex(r"$\therefore BE = AC = 4$", font_size=28, color="#2ecc71")
        
        answer = Tex(r"答：当 $D$ 为 $AB$ 中点时，$BE = 4$", font_size=28, color="#2ecc71")
        
        content = VGroup(
            title,
            step1, pythagoras, calc1, result1,
            step2, midpoint, result2,
            step3, congruent2, final,
            answer
        ).arrange(DOWN, buff=0.25).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(step1), Write(pythagoras), Write(calc1), Write(result1))
        self.play(Write(step2), Write(midpoint), Write(result2))
        self.play(Write(step3), Write(congruent2), Write(final))
        self.play(Write(answer))
        self.wait_for_audio(5, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_6_q3_1_setup(self):
        """第 6 幕：第 3 问①分析"""
        self.add_scene_audio(6)
        
        title = Tex(r"第 (3) 问①：求证 $CE^2 = 2BD \cdot AD$", font_size=36)
        
        idea = Tex(r"思路：在 Rt$\triangle CDE$ 中，$CD = DE$")
        pythagoras2 = Tex(r"由勾股定理：$CE^2 = CD^2 + DE^2 = 2CD^2$")
        key = Tex(r"关键：证明 $CD^2 = BD \cdot AD$", font_size=26, color="#f39c12")
        method = Tex(r"方法：相似三角形 $\triangle ACD \sim \triangle CBD$")
        
        content = VGroup(title, idea, pythagoras2, key, method).arrange(DOWN, buff=0.35).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(idea), Write(pythagoras2))
        self.play(Write(key))
        self.play(Write(method))
        self.wait_for_audio(6, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_7_q3_1_proof(self):
        """第 7 幕：第 3 问①证明"""
        self.add_scene_audio(7)
        
        title = Text("证明：", font_size=44, color="#3498db")
        
        step1 = Tex(r"在 Rt$\triangle CDE$ 中：", font_size=26)
        pythagoras3 = Tex(r"$CE^2 = CD^2 + DE^2$（勾股定理）")
        equal = Tex(r"$= CD^2 + CD^2$（$\because CD = DE$）")
        result1 = Tex(r"$= 2CD^2$")
        
        step2 = Tex(r"证明 $CD^2 = BD \cdot AD$：", font_size=26)
        similar = Tex(r"在 $\triangle ACD$ 和 $\triangle CBD$ 中：")
        angle1 = Tex(r"$\angle A = \angle BCD$（同角的余角相等）")
        angle2 = Tex(r"$\angle ADC = \angle CDB$（公共角）")
        congruent3 = Tex(r"$\therefore \triangle ACD \sim \triangle CBD$（AA）")
        ratio = Tex(r"$\therefore \frac{AD}{CD} = \frac{CD}{BD}$")
        result2 = Tex(r"即 $CD^2 = BD \cdot AD$")
        
        final = Tex(r"$\therefore CE^2 = 2CD^2 = 2BD \cdot AD$  得证", 
                   font_size=28, color="#2ecc71")
        
        content = VGroup(
            title,
            step1, pythagoras3, equal, result1,
            step2, similar, angle1, angle2, congruent3, ratio, result2,
            final
        ).arrange(DOWN, buff=0.2).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(step1), Write(pythagoras3), Write(equal), Write(result1))
        self.play(Write(step2), Write(similar))
        self.play(Write(angle1), Write(angle2))
        self.play(Write(congruent3), Write(ratio), Write(result2))
        self.play(Write(final))
        self.wait_for_audio(7, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_8_q3_2_solve(self):
        """第 8 幕：第 3 问②求解"""
        self.add_scene_audio(8)
        
        title = Tex(r"第 (3) 问②：求 $CE$ 的最小值", font_size=36)
        
        step1 = Tex(r"由①知：$CE^2 = 2BD \cdot AD$")
        
        step2 = Tex(r"设 $AD = x$，则 $BD = 5 - x$（$\because AB = 5$）")
        
        function = Tex(r"$CE^2 = 2(5-x) \cdot x = 2(5x - x^2) = -2x^2 + 10x$")
        
        analysis = Tex(r"这是关于 $x$ 的二次函数，开口向下，有最大值")
        
        vertex = Tex(r"当 $x = -\frac{b}{2a} = -\frac{10}{-4} = 2.5$ 时")
        
        max_val = Tex(r"$CE^2$ 有最大值 $= -2(2.5)^2 + 10(2.5) = 12.5$")
        
        final = Tex(r"$\therefore CE$ 的最小值 $= \sqrt{12.5} = \frac{5\sqrt{2}}{2}$", 
                   font_size=28, color="#2ecc71")
        
        note = Tex(r"此时 $D$ 为 $AB$ 中点")
        
        content = VGroup(
            title,
            step1,
            step2,
            function,
            analysis,
            vertex,
            max_val,
            final,
            note
        ).arrange(DOWN, buff=0.25).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(step1))
        self.play(Write(step2))
        self.play(Write(function))
        self.play(Write(analysis))
        self.play(Write(vertex), Write(max_val))
        self.play(Write(final), Write(note))
        self.wait_for_audio(8, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_9_summary(self):
        """第 9 幕：答案汇总"""
        self.add_scene_audio(9)
        
        title = Text("答案汇总", font_size=48, color="#3498db")
        
        ans1 = Tex(r"(1) 证明：$\triangle ACD \cong \triangle BED$（SAS）")
        ans1_result = Tex(r"$\therefore \angle ABE = 90^\circ$")
        
        ans2 = Tex(r"(2) $BE = 4$", font_size=28, color="#2ecc71")
        
        ans3_1 = Tex(r"(3) ① 证明：$CE^2 = 2BD \cdot AD$")
        ans3_2 = Tex(r"② $CE$ 的最小值 $= \frac{5\sqrt{2}}{2}$", font_size=28, color="#2ecc71")
        
        method_title = Text("解题方法总结：", font_size=28, color="#f39c12")
        method1 = Text("1. 旋转全等 → 证明垂直", font_size=22)
        method2 = Text("2. 勾股定理 → 求边长", font_size=22)
        method3 = Text("3. 相似三角形 → 建立关系", font_size=22)
        method4 = Text("4. 二次函数 → 求最值", font_size=22)
        
        thanks = Text("谢谢观看！", font_size=48, color="#3498db")
        
        content = VGroup(
            title,
            ans1, ans1_result,
            ans2,
            ans3_1, ans3_2,
            method_title, method1, method2, method3, method4,
            thanks
        ).arrange(DOWN, buff=0.3).center()
        
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(ans1), Write(ans1_result))
        self.play(Write(ans2))
        self.play(Write(ans3_1), Write(ans3_2))
        self.play(Write(method_title), Write(method1), Write(method2), Write(method3), Write(method4))
        self.play(Write(thanks))
        self.wait_for_audio(9, self.time - start_time)
        self.play(FadeOut(content))


if __name__ == "__main__":
    scene = GeometryRotationProblem()
    scene.render()
