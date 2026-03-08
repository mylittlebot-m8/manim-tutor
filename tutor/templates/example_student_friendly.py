"""
学生友好型脚本示例 - 详细讲解版

核心原则：
1. 每一步都解释"为什么"
2. 不跳步，展示完整推导
3. 关键步骤用颜色/大小突出
4. 每幕结束有小结
"""

from manim import *
import json
from pathlib import Path


class StudentFriendlyParabola(Scene):
    """抛物线综合题 - 学生友好版"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        self.script_dir = Path(__file__).parent
        self.audio_dir = self._find_audio_dir()
        self.audio_timings = self.load_audio_timings()
        
        self.scene_1_intro()
        self.scene_2_find_AB()
        self.scene_3_find_CD()
        self.scene_4_summary()
    
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
    
    def scene_1_intro(self):
        """第 1 幕：题目介绍（详细说明）"""
        self.add_scene_audio(1)
        
        # 标题
        title = Text("抛物线综合题", font_size=48, color="#3498db")
        
        # 题目内容 - 分行显示，便于阅读
        problem_intro = Text("已知抛物线方程：", font_size=28)
        problem_formula = MathTex(r"y = -x^2 + 2x + 3", font_size=32, color=WHITE)
        
        # 问题列表 - 逐题显示
        q1_title = Text("第 (1) 问：", font_size=26, color="#f39c12")
        q1_content = Text("求 A、B、C、D 四点的坐标", font_size=24)
        
        q2_title = Text("第 (2) 问：", font_size=26, color="#f39c12")
        q2_content = Text("求△PAC 面积最大时的 P 点坐标及最大面积", font_size=24)
        
        q3_title = Text("第 (3) 问：", font_size=26, color="#f39c12")
        q3_content = Text("对称轴上是否存在点 Q，使△QBC 为等腰三角形？", font_size=24)
        
        # 组合
        content = VGroup(
            title,
            VGroup(problem_intro, problem_formula).arrange(DOWN, buff=0.3),
            VGroup(q1_title, q1_content).arrange(RIGHT, buff=0.2),
            VGroup(q2_title, q2_content).arrange(RIGHT, buff=0.2),
            VGroup(q3_title, q3_content).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.4).center()
        
        # 动画 - 逐步显示
        start_time = self.time
        self.play(FadeIn(title))
        self.play(FadeIn(problem_intro), FadeIn(problem_formula))
        self.play(FadeIn(q1_title), FadeIn(q1_content))
        self.play(FadeIn(q2_title), FadeIn(q2_content))
        self.play(FadeIn(q3_title), FadeIn(q3_content))
        
        # 小结
        summary = Text("提示：先求与坐标轴的交点，再求顶点坐标", 
                      font_size=22, color="#2ecc71")
        summary.next_to(content, DOWN, buff=0.5)
        self.play(Write(summary))
        
        self.wait_for_audio(1, self.time - start_time)
        self.play(FadeOut(content), FadeOut(summary))
    
    def scene_2_find_AB(self):
        """第 2 幕：求 A、B 坐标（详细步骤）"""
        self.add_scene_audio(2)
        
        # 标题
        title = Text("第 (1) 问：求 A、B 坐标", font_size=40, color="#3498db")
        
        # 步骤 1：说明思路
        step1_title = Text("思路分析：", font_size=28, color="#f39c12")
        step1_detail = Text("A、B 是抛物线与 x 轴的交点，所以 y 坐标为 0", 
                           font_size=22, color="#7f8c8d")
        
        # 步骤 2：列方程
        step2_title = Text("步骤 1：令 y = 0，解方程", font_size=28, color="#3498db")
        eq1 = MathTex(r"-x^2 + 2x + 3 = 0", font_size=28)
        
        # 步骤 3：整理方程
        step3_title = Text("步骤 2：整理方程（两边乘以 -1）", font_size=24, color="#95a5a6")
        eq2 = MathTex(r"x^2 - 2x - 3 = 0", font_size=28)
        
        # 步骤 4：因式分解
        step4_title = Text("步骤 3：因式分解", font_size=24, color="#95a5a6")
        step4_detail = Text("找两个数，乘积为 -3，和为 -2", 
                           font_size=20, color="#7f8c8d")
        eq3 = MathTex(r"(x-3)(x+1) = 0", font_size=28, color="#f39c12")
        
        # 步骤 5：求解
        step5_title = Text("步骤 4：解得 x 的值", font_size=24, color="#95a5a6")
        eq4 = MathTex(r"x_1 = 3, \quad x_2 = -1", font_size=28)
        
        # 结论
        conclusion = Text("∴ A(-1, 0), B(3, 0)", font_size=32, color="#2ecc71")
        
        # 组合
        content = VGroup(
            title,
            VGroup(step1_title, step1_detail).arrange(DOWN, buff=0.3),
            VGroup(step2_title, eq1).arrange(DOWN, buff=0.3),
            VGroup(step3_title, eq2).arrange(DOWN, buff=0.3),
            VGroup(step4_title, step4_detail, eq3).arrange(DOWN, buff=0.3),
            VGroup(step5_title, eq4).arrange(DOWN, buff=0.3),
            conclusion
        ).arrange(DOWN, buff=0.35).center()
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(step1_title), Write(step1_detail))
        self.play(Write(step2_title), Write(eq1))
        self.play(Write(step3_title), Write(eq2))
        self.play(Write(step4_title), Write(step4_detail), Write(eq3))
        self.play(Write(step5_title), Write(eq4))
        self.play(Write(conclusion))
        
        self.wait_for_audio(2, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_3_find_CD(self):
        """第 3 幕：求 C、D 坐标（详细步骤）"""
        self.add_scene_audio(3)
        
        title = Text("求 C、D 坐标", font_size=40, color="#3498db")
        
        # C 点部分
        c_section = VGroup(
            Text("【求 C 点坐标】", font_size=28, color="#3498db"),
            Text("C 点是抛物线与 y 轴的交点", font_size=22, color="#7f8c8d"),
            Text("所以 x 坐标为 0，代入方程求 y：", font_size=22, color="#7f8c8d"),
            MathTex(r"x = 0", font_size=26),
            MathTex(r"y = -0^2 + 2\\cdot 0 + 3 = 3", font_size=26),
            Text("∴ C(0, 3)", font_size=28, color="#2ecc71")
        ).arrange(DOWN, buff=0.3)
        
        # D 点部分
        d_section = VGroup(
            Text("【求顶点 D 坐标】", font_size=28, color="#3498db"),
            Text("顶点横坐标公式：", font_size=22, color="#7f8c8d"),
            MathTex(r"x = -\frac{b}{2a}", font_size=26),
            Text("代入 a = -1, b = 2：", font_size=22, color="#7f8c8d"),
            MathTex(r"x = -\frac{2}{2\\cdot(-1)} = 1", font_size=26),
            Text("将 x = 1 代入原方程求 y：", font_size=22, color="#7f8c8d"),
            MathTex(r"y = -1^2 + 2\\cdot 1 + 3 = 4", font_size=26),
            Text("∴ D(1, 4)", font_size=28, color="#2ecc71")
        ).arrange(DOWN, buff=0.3)
        
        content = VGroup(title, c_section, d_section).arrange(DOWN, buff=0.5).center()
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(c_section))
        self.play(Write(d_section))
        
        self.wait_for_audio(3, self.time - start_time)
        self.play(FadeOut(content))
    
    def scene_4_summary(self):
        """第 4 幕：本问小结"""
        self.add_scene_audio(4)
        
        title = Text("第 (1) 问 小结", font_size=44, color="#3498db")
        
        # 答案汇总
        answer_box = VGroup(
            Text("答案：", font_size=32, color="#f39c12"),
            MathTex(r"A(-1, 0)", font_size=28),
            MathTex(r"B(3, 0)", font_size=28),
            MathTex(r"C(0, 3)", font_size=28),
            MathTex(r"D(1, 4)", font_size=28)
        ).arrange(DOWN, buff=0.4)
        
        # 方法总结
        method_title = Text("解题方法：", font_size=28, color="#f39c12")
        method_1 = Text("1. 与 x 轴交点 → 令 y = 0，解方程", font_size=22)
        method_2 = Text("2. 与 y 轴交点 → 令 x = 0，代入求 y", font_size=22)
        method_3 = Text("3. 顶点坐标 → 使用顶点公式", font_size=22)
        
        method_summary = VGroup(method_title, method_1, method_2, method_3).arrange(DOWN, buff=0.3)
        
        content = VGroup(title, answer_box, method_summary).arrange(DOWN, buff=0.5).center()
        
        # 动画
        start_time = self.time
        self.play(FadeIn(title))
        self.play(Write(answer_box))
        self.play(Write(method_summary))
        
        self.wait_for_audio(4, self.time - start_time)
        self.play(FadeOut(content))


# 运行示例
if __name__ == "__main__":
    # 这是示例，实际需要 audio 目录和 audio_info.json
    print("学生友好型脚本示例")
    print("请确保 audio 目录存在并包含音频文件")
