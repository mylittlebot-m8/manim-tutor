"""
文创店采购问题 - Manim动画（无LaTeX版本）
"""

from manim import *
import json
from pathlib import Path

class DollProblemScene(Scene):
    """文创店采购问题教学场景"""
    
    def construct(self):
        # 设置背景
        self.camera.background_color = "#1a1a2e"
        
        # 获取当前文件所在目录
        self.script_dir = Path(__file__).parent
        
        # 加载音频时长信息（如果存在）
        try:
            audio_info_path = self.script_dir / "audio" / "audio_info.json"
            with open(audio_info_path, "r") as f:
                audio_info = json.load(f)
                self.audio_timings = {item["scene"]: item["duration"] for item in audio_info["files"]}
        except:
            self.audio_timings = {1: 5.0, 2: 8.0, 3: 10.0, 4: 8.0, 5: 10.0, 6: 7.0, 7: 12.0, 8: 8.0}
        
        # 第1幕：开场
        self.play_scene_1()
        
        # 第2幕：第1问分析
        self.play_scene_2()
        
        # 第3幕：第1问求解
        self.play_scene_3()
        
        # 第4幕：第2问分析
        self.play_scene_4()
        
        # 第5幕：第2问求解
        self.play_scene_5()
        
        # 第6幕：第3问分析
        self.play_scene_6()
        
        # 第7幕：第3问求解
        self.play_scene_7()
        
        # 第8幕：总结
        self.play_scene_8()
    
    def play_scene_1(self):
        """第1幕：开场"""
        audio_file = self.script_dir / "audio" / "audio_001_开场.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("文创店采购问题", font_size=48, color="#3498db")
        subtitle = Text("应用题解析", font_size=24, color="#7f8c8d")
        subtitle.next_to(title, DOWN)
        
        self.play(FadeIn(title), FadeIn(subtitle))
        duration = self.audio_timings.get(1, 5.0)
        self.wait(duration)
        self.play(FadeOut(title), FadeOut(subtitle))
    
    def play_scene_2(self):
        """第2幕：第1问分析"""
        audio_file = self.script_dir / "audio" / "audio_002_第1问分析.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        var_text = VGroup(
            Text("设萌系公仔单价为 x 元", font_size=28, color=WHITE),
            Text("设喜庆公仔单价为 y 元", font_size=28, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT)
        var_text.to_edge(UP)
        
        # 使用普通文本代替MathTex
        eq1 = Text("20x + 30y = 2100", font_size=32, color="#e74c3c", font="Courier New")
        eq2 = Text("30x + 10y = 1400", font_size=32, color="#e74c3c", font="Courier New")
        equations = VGroup(eq1, eq2).arrange(DOWN, buff=0.5)
        equations.center()
        
        self.play(Write(var_text))
        self.wait(1)
        self.play(Write(eq1))
        self.wait(1)
        self.play(Write(eq2))
        
        duration = self.audio_timings.get(2, 8.0)
        elapsed = 3
        if duration > elapsed:
            self.wait(duration - elapsed)
        self.play(FadeOut(var_text), FadeOut(equations))
    
    def play_scene_3(self):
        """第3幕：第1问求解"""
        audio_file = self.script_dir / "audio" / "audio_003_第1问求解.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        step1 = Text("② × 3 - ①: 70x = 2100", font_size=28, color=WHITE)
        step2 = Text("x = 30", font_size=36, color="#2ecc71")
        step3 = Text("代入: y = 50", font_size=36, color="#2ecc71")
        
        answer = VGroup(
            Text("萌系公仔: 30元/个", font_size=28, color="#2ecc71"),
            Text("喜庆公仔: 50元/个", font_size=28, color="#2ecc71")
        ).arrange(DOWN)
        
        self.play(Write(step1))
        self.wait(1.5)
        self.play(Transform(step1, step2))
        self.wait(1.5)
        self.play(FadeOut(step1))
        self.play(Write(step3))
        self.wait(1.5)
        self.play(FadeOut(step3))
        self.play(Write(answer))
        
        duration = self.audio_timings.get(3, 10.0)
        elapsed = 5
        if duration > elapsed:
            self.wait(duration - elapsed)
        self.play(FadeOut(answer))
    
    def play_scene_4(self):
        """第4幕：第2问分析"""
        audio_file = self.script_dir / "audio" / "audio_004_第2问分析.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        content = VGroup(
            Text("总数量: 100个", font_size=28, color=WHITE),
            Text("萌系: m 个", font_size=28, color="#3498db"),
            Text("喜庆: (100-m) 个", font_size=28, color="#e74c3c"),
            Text("利润要求: ≥ 2400元", font_size=28, color="#f39c12")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        content.center()
        
        self.play(Write(content))
        duration = self.audio_timings.get(4, 8.0)
        self.wait(duration)
        self.play(FadeOut(content))
    
    def play_scene_5(self):
        """第5幕：第2问求解"""
        audio_file = self.script_dir / "audio" / "audio_005_第2问求解.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        profit_eq = Text("总利润 = 20m + 30(100-m) ≥ 2400", font_size=26, color=WHITE)
        simplify = Text("3000 - 10m ≥ 2400", font_size=28, color="#f39c12")
        result = Text("m ≤ 60", font_size=36, color="#2ecc71")
        answer = Text("最多采购60个萌系公仔", font_size=32, color="#2ecc71")
        
        self.play(Write(profit_eq))
        self.wait(2)
        self.play(Transform(profit_eq, simplify))
        self.wait(2)
        self.play(Transform(profit_eq, result))
        self.wait(2)
        self.play(FadeOut(profit_eq))
        self.play(Write(answer))
        
        duration = self.audio_timings.get(5, 10.0)
        elapsed = 6
        if duration > elapsed:
            self.wait(duration - elapsed)
        self.play(FadeOut(answer))
    
    def play_scene_6(self):
        """第6幕：第3问分析"""
        audio_file = self.script_dir / "audio" / "audio_006_第3问分析.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        original = VGroup(
            Text("原价: 80元", font_size=28, color=WHITE),
            Text("销量: 40个/天", font_size=28, color=WHITE)
        ).arrange(DOWN)
        
        arrow = Arrow(ORIGIN, RIGHT*2, color="#f39c12")
        
        after = VGroup(
            Text("降价 a 元", font_size=28, color="#e74c3c"),
            Text("销量: 40+2a 个", font_size=28, color="#2ecc71")
        ).arrange(DOWN)
        
        VGroup(original, arrow, after).arrange(RIGHT, buff=1)
        
        self.play(Write(original))
        self.wait(1)
        self.play(GrowArrow(arrow))
        self.play(Write(after))
        
        duration = self.audio_timings.get(6, 7.0)
        elapsed = 3
        if duration > elapsed:
            self.wait(duration - elapsed)
        self.play(FadeOut(original), FadeOut(arrow), FadeOut(after))
    
    def play_scene_7(self):
        """第7幕：第3问求解"""
        audio_file = self.script_dir / "audio" / "audio_007_第3问求解.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        eq = Text("(30-a)(40+2a) = 1200", font_size=28, color=WHITE)
        expand = Text("展开化简: 20a - 2a² = 0", font_size=26, color="#f39c12")
        factor = Text("2a(10-a) = 0", font_size=28, color="#9b59b6")
        solution = Text("a = 10", font_size=36, color="#2ecc71")
        price = Text("售价定为: 70元", font_size=32, color="#2ecc71")
        
        self.play(Write(eq))
        self.wait(1.5)
        self.play(Transform(eq, expand))
        self.wait(1.5)
        self.play(Transform(eq, factor))
        self.wait(1.5)
        self.play(Transform(eq, solution))
        self.wait(1.5)
        self.play(FadeOut(eq))
        self.play(Write(price))
        
        duration = self.audio_timings.get(7, 12.0)
        elapsed = 7
        if duration > elapsed:
            self.wait(duration - elapsed)
        self.play(FadeOut(price))
    
    def play_scene_8(self):
        """第8幕：总结"""
        audio_file = self.script_dir / "audio" / "audio_008_总结.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        answers = VGroup(
            Text("(1) 萌系30元，喜庆50元", font_size=26, color="#3498db"),
            Text("(2) 最多60个萌系", font_size=26, color="#e74c3c"),
            Text("(3) 售价70元", font_size=26, color="#2ecc71")
        ).arrange(DOWN, buff=0.8)
        
        methods = VGroup(
            Text("方程组 → 不等式 → 二次方程", font_size=22, color="#f39c12"),
            Text("综合应用能力", font_size=22, color="#9b59b6")
        ).arrange(DOWN)
        methods.next_to(answers, DOWN, buff=1)
        
        self.play(Write(answers))
        self.wait(2)
        self.play(Write(methods))
        
        duration = self.audio_timings.get(8, 8.0)
        elapsed = 4
        if duration > elapsed:
            self.wait(duration - elapsed)
        self.play(FadeOut(answers), FadeOut(methods))
