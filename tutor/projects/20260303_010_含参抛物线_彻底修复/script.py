"""
教学视频脚本模板 - 带题目朗读
根据分镜自动生成，包含题目显示和 TTS 音频同步
"""

from manim import *
import json
from pathlib import Path


class TeachingScene(Scene):
    """教学场景基类"""
    
    def construct(self):
        # 设置背景
        self.camera.background_color = "#1a1a2e"
        
        # 获取脚本目录
        self.script_dir = Path(__file__).parent
        
        # 智能检测音频目录（支持多种部署结构）
        self.audio_dir = self._find_audio_dir()
        
        # 加载音频时长
        self.audio_timings = self.load_audio_timings()
        
        # 执行各幕
        self.play_scene_1()  # 题目朗读
        self.play_scene_2()  # 问题分析
        self.play_scene_3()  # 建立模型
        self.play_scene_4()  # 求解过程
        self.play_scene_5()  # 验证答案
        self.play_scene_6()  # 总结
    
    def _find_audio_dir(self):
        """智能查找音频目录"""
        candidates = [
            Path(__file__).parent / "audio",
            Path(__file__).parent.parent / "audio",
            Path(__file__).parent / ".." / "audio",
        ]
        
        for candidate in candidates:
            if candidate.exists() and any(candidate.glob("*.wav")):
                return candidate
        
        return Path(__file__).parent / "audio"
    
    def load_audio_timings(self):
        """加载音频时长信息"""
        if not self.audio_dir or not self.audio_dir.exists():
            return {i: 10.0 for i in range(1, 20)}
        
        try:
            audio_info_path = self.audio_dir / "audio_info.json"
            with open(audio_info_path, "r") as f:
                audio_info = json.load(f)
                return {item["scene"]: item["duration"] for item in audio_info["files"]}
        except:
            return {i: 10.0 for i in range(1, 20)}
    
    def play_scene_1(self):
        """第 1 幕：题目朗读"""
        audio_file = self.audio_dir / "audio_001_scene.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        # 硬编码题目文本 - 不依赖 storyboard.md
        problem_text = self._get_problem_text_from_audio()
        
        title = Text("题目", font_size=36, color="#3498db")
        title.to_edge(UP, buff=0.5)
        
        lines = self._wrap_text(problem_text, max_chars=25)
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
    
    def _get_problem_text_from_audio(self):
        """从音频文件名推断题目（简单方法）"""
        # 检查 audio_info.json
        try:
            audio_info_path = self.audio_dir / "audio_info.json"
            if audio_info_path.exists():
                with open(audio_info_path, "r") as f:
                    audio_info = json.load(f)
                    # 返回第一个音频的描述作为题目
                    if audio_info.get("files"):
                        return audio_info["files"][0].get("text", "数学题目")
        except:
            pass
        return "数学题目"
    
    def _wrap_text(self, text, max_chars=25):
        """文本分行"""
        words = text.replace(',', ' ').replace(';', ' ').split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines if lines else [text]
    
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
