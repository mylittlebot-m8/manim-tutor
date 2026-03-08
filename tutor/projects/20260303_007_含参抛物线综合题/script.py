"""
教学视频脚本模板 - 带题目朗读
根据分镜自动生成，包含题目显示和TTS音频同步
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
    
    def _find_audio_dir(self):
        """智能查找音频目录"""
        # 尝试多个可能的位置
        candidates = [
            Path(__file__).parent / "audio",                    # 同级目录
            Path(__file__).parent.parent / "audio",             # 父目录
            Path(__file__).parent / ".." / "audio",             # 相对路径
        ]
        
        for candidate in candidates:
            if candidate.exists() and any(candidate.glob("*.wav")):
                return candidate
        
        # 默认返回同级目录
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
    
    def play_scene_1(self):
        """第1幕：题目朗读"""
        # 添加音频
        audio_file = self.audio_dir / "audio_001_题目朗读.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        # 读取题目文本
        problem_text = self.get_problem_text()
        
        # 标题
        title = Text("题目", font_size=36, color="#3498db")
        title.to_edge(UP, buff=0.5)
        
        # 题目内容（分段显示，避免太长）
        lines = self.wrap_text(problem_text, max_chars=25)
        problem_lines = VGroup(*[
            Text(line, font_size=20, color=WHITE)
            for line in lines[:8]  # 最多显示8行
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        problem_lines.next_to(title, DOWN, buff=0.5)
        
        # 动画
        self.play(FadeIn(title))
        self.wait(0.5)
        
        # 逐行显示题目
        for line in problem_lines:
            self.play(FadeIn(line, run_time=0.8))
            self.wait(0.2)
        
        # 等待音频结束
        duration = self.audio_timings.get(1, 15.0)
        elapsed = len(problem_lines) * 1.0 + 1.0
        if duration > elapsed:
            self.wait(duration - elapsed)
        
        self.play(FadeOut(title), FadeOut(problem_lines))
    
    def play_scene_2(self):
        """第2幕：问题分析"""
        audio_file = self.audio_dir / "audio_002_问题分析.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("问题分析", font_size=40, color="#3498db")
        subtitle = Text("明确已知条件和求解目标", font_size=24, color="#7f8c8d")
        subtitle.next_to(title, DOWN)
        
        content = Text("分析中...", font_size=28, color=WHITE)
        content.center()
        
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(1)
        self.play(Write(content))
        
        duration = self.audio_timings.get(2, 8.0)
        self.wait(duration)
        
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(content))
    
    def play_scene_3(self):
        """第3幕：建立模型"""
        audio_file = self.audio_dir / "audio_003_建立模型.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("建立数学模型", font_size=40, color="#3498db")
        title.to_edge(UP)
        
        model_text = Text("设未知数，列方程...", font_size=28, color="#e74c3c")
        model_text.center()
        
        self.play(FadeIn(title))
        self.wait(0.5)
        self.play(Write(model_text))
        
        duration = self.audio_timings.get(3, 8.0)
        self.wait(duration)
        
        self.play(FadeOut(title), FadeOut(model_text))
    
    def play_scene_4(self):
        """第4幕：求解过程"""
        audio_file = self.audio_dir / "audio_004_求解过程.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("求解过程", font_size=40, color="#3498db")
        title.to_edge(UP)
        
        steps = VGroup(
            Text("步骤1: ...", font_size=24, color=WHITE),
            Text("步骤2: ...", font_size=24, color=WHITE),
            Text("步骤3: 得出结果", font_size=24, color="#2ecc71")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        steps.center()
        
        self.play(FadeIn(title))
        self.wait(0.5)
        
        for step in steps:
            self.play(Write(step))
            self.wait(1)
        
        duration = self.audio_timings.get(4, 12.0)
        elapsed = len(steps) * 1.5 + 1.0
        if duration > elapsed:
            self.wait(duration - elapsed)
        
        self.play(FadeOut(title), FadeOut(steps))
    
    def play_scene_5(self):
        """第5幕：验证答案"""
        audio_file = self.audio_dir / "audio_005_验证答案.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("验证答案", font_size=40, color="#3498db")
        check = Text("✓ 答案正确", font_size=36, color="#2ecc71")
        
        self.play(FadeIn(title))
        self.wait(1)
        self.play(Write(check))
        
        duration = self.audio_timings.get(5, 6.0)
        self.wait(duration)
        
        self.play(FadeOut(title), FadeOut(check))
    
    def play_scene_6(self):
        """第6幕：总结"""
        audio_file = self.audio_dir / "audio_006_总结.wav"
        if audio_file.exists():
            self.add_sound(str(audio_file))
        
        title = Text("方法总结", font_size=40, color="#3498db")
        title.to_edge(UP)
        
        summary = VGroup(
            Text("解题方法: ...", font_size=26, color="#f39c12"),
            Text("关键步骤: ...", font_size=26, color="#9b59b6")
        ).arrange(DOWN, buff=0.8)
        summary.center()
        
        self.play(FadeIn(title))
        self.wait(1)
        self.play(Write(summary))
        
        duration = self.audio_timings.get(6, 8.0)
        self.wait(duration)
        
        self.play(FadeOut(title), FadeOut(summary))
    
    def get_problem_text(self) -> str:
        """从storyboard.md读取题目文本"""
        try:
            storyboard_path = self.script_dir / "storyboard.md"
            content = storyboard_path.read_text(encoding='utf-8')
            
            # 提取第1幕的读白内容
            match = re.search(r'### 第1幕.*?\*\*读白\*\*:\s*"([^"]+)"', content, re.DOTALL)
            if match:
                return match.group(1)
        except:
            pass
        
        return "题目内容"
    
    def wrap_text(self, text: str, max_chars: int = 25) -> list:
        """将长文本分行"""
        words = text.replace('，', ' ').replace('。', ' ').replace('；', ' ').split()
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
