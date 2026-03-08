"""
教学视频脚本模板 - 带题目朗读
从 storyboard.md 读取题目内容
"""

from manim import *
import json
import re
from pathlib import Path


class TeachingScene(Scene):
    """教学场景基类"""
    
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        self.script_dir = Path(__file__).parent
        self.audio_dir = self._find_audio_dir()
        self.audio_timings = self.load_audio_timings()
        
        # 从 storyboard.md 读取题目文本
        self.problem_text = self._get_problem_text_from_storyboard()
        
        # 执行各幕
        self.play_scene_1()
        self.play_scene_2()
        self.play_scene_3()
        self.play_scene_4()
        self.play_scene_5()
        self.play_scene_6()
    
    def _find_audio_dir(self):
        candidates = [
            Path(__file__).parent / "audio",
            Path(__file__).parent.parent / "audio",
        ]
        for c in candidates:
            if c.exists() and any(c.glob("*.wav")):
                return c
        return Path(__file__).parent / "audio"
    
    def load_audio_timings(self):
        if not self.audio_dir or not self.audio_dir.exists():
            return {i: 10.0 for i in range(1, 20)}
        try:
            with open(self.audio_dir / "audio_info.json", "r") as f:
                audio_info = json.load(f)
                return {item["scene"]: item["duration"] for item in audio_info["files"]}
        except:
            return {i: 10.0 for i in range(1, 20)}
    
    def _get_problem_text_from_storyboard(self):
        """从 storyboard.md 读取题目文本"""
        storyboard_path = Path(__file__).parent / "storyboard.md"
        if not storyboard_path.exists():
            return "数学题目"
        
        try:
            with open(storyboard_path, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r'\*\*读白\*\*:\s*"([^"]+)"', content)
                if match:
                    return match.group(1)
        except Exception as e:
            print(f"[ERROR] 读取 storyboard 失败：{e}")
        return "数学题目"
    
    def _wrap_text(self, text, max_chars=25):
        words = text.replace(',', ' ').replace(';', ' ').split()
        lines = []
        current = ""
        for w in words:
            if len(current) + len(w) + 1 <= max_chars:
                current += w + " "
            else:
                if current:
                    lines.append(current.strip())
                current = w + " "
        if current:
            lines.append(current.strip())
        return lines if lines else [text]
    
    def play_scene_1(self):
        """第 1 幕：题目朗读"""
        audio_file = self.audio_dir / "audio_001_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("题目", font_size=36, color="#3498db")
        title.to_edge(UP, buff=0.5)
        
        lines = self._wrap_text(self.problem_text, max_chars=25)
        problem_lines = VGroup(*[
            Text(line, font_size=20, color=WHITE)
            for line in lines[:8]
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        problem_lines.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(title))
        self.wait(0.5)
        for line in problem_lines:
            self.play(FadeIn(line, run_time=0.8))
            self.wait(0.2)
        
        duration = self.audio_timings.get(1, 15.0)
        elapsed = len(problem_lines) * 1.0 + 1.0
        if duration > elapsed:
            self.wait(duration - elapsed)
        
        self.play(FadeOut(title), FadeOut(problem_lines))
    
    def play_scene_2(self):
        """第 2 幕：问题分析"""
        audio_file = self.audio_dir / "audio_002_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("问题分析", font_size=40, color="#3498db")
        content = Text("分析已知条件和求解目标", font_size=28, color=WHITE)
        VGroup(title, content).arrange(DOWN, buff=0.8).center()
        
        self.play(FadeIn(title))
        self.play(Write(content))
        duration = self.audio_timings.get(2, 8.0)
        self.wait(duration)
        self.play(FadeOut(title), FadeOut(content))
    
    def play_scene_3(self):
        """第 3 幕：建立模型"""
        audio_file = self.audio_dir / "audio_003_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("建立模型", font_size=40, color="#3498db")
        content = Text("设定变量，建立方程", font_size=28, color=WHITE)
        VGroup(title, content).arrange(DOWN, buff=0.8).center()
        
        self.play(FadeIn(title))
        self.play(Write(content))
        duration = self.audio_timings.get(3, 8.0)
        self.wait(duration)
        self.play(FadeOut(title), FadeOut(content))
    
    def play_scene_4(self):
        """第 4 幕：求解过程"""
        audio_file = self.audio_dir / "audio_004_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("求解过程", font_size=40, color="#3498db")
        content = Text("逐步推导，得出结果", font_size=28, color=WHITE)
        VGroup(title, content).arrange(DOWN, buff=0.8).center()
        
        self.play(FadeIn(title))
        self.play(Write(content))
        duration = self.audio_timings.get(4, 12.0)
        self.wait(duration)
        self.play(FadeOut(title), FadeOut(content))
    
    def play_scene_5(self):
        """第 5 幕：验证答案"""
        audio_file = self.audio_dir / "audio_005_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("验证答案", font_size=40, color="#3498db")
        content = Text("检查答案是否符合题意", font_size=28, color=WHITE)
        VGroup(title, content).arrange(DOWN, buff=0.8).center()
        
        self.play(FadeIn(title))
        self.play(Write(content))
        duration = self.audio_timings.get(5, 6.0)
        self.wait(duration)
        self.play(FadeOut(title), FadeOut(content))
    
    def play_scene_6(self):
        """第 6 幕：总结"""
        audio_file = self.audio_dir / "audio_006_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("总结", font_size=44, color="#3498db")
        content = Text("回顾解题方法和关键点", font_size=28, color=WHITE)
        VGroup(title, content).arrange(DOWN, buff=0.8).center()
        
        self.play(FadeIn(title))
        self.play(Write(content))
        duration = self.audio_timings.get(6, 8.0)
        self.wait(duration)
        self.play(FadeOut(title), FadeOut(content))
