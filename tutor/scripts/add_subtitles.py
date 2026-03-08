#!/usr/bin/env python3
"""
为视频添加 TTS 同步字幕
用法：python add_subtitles.py <video.mp4> <audio_info.json> [output.mp4]
"""

import json
import subprocess
from pathlib import Path


def time_to_ass(seconds):
    """将秒数转换为 ASS 时间格式：H:MM:SS.cc"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centiseconds = int((seconds % 1) * 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"


def generate_ass_subtitles(audio_info_path, output_path):
    """生成 ASS 字幕文件"""
    
    # 读取 audio_info.json
    with open(audio_info_path, 'r', encoding='utf-8') as f:
        audio_info = json.load(f)
    
    files = audio_info.get('files', [])
    
    # ASS 文件头
    ass_content = """[Script Info]
Title: 几何旋转综合题
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
Timer: 100.0000

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft YaHei,32,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    # 生成字幕
    current_time = 0.0
    
    for i, file_info in enumerate(files):
        duration = file_info.get('duration', 0)
        text = file_info.get('text', '')
        
        # 跳过没有文本的音频
        if not text or duration == 0:
            continue
        
        start_time = current_time
        end_time = current_time + duration
        
        # 转换为 ASS 时间格式
        start_ass = time_to_ass(start_time)
        end_ass = time_to_ass(end_time)
        
        # 添加字幕行
        ass_content += f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{text}\n"
        
        current_time = end_time
    
    # 保存 ASS 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ass_content)
    
    print(f"✅ ASS 字幕已生成：{output_path}")
    print(f"   共 {len(files)} 条字幕")
    print(f"   总时长：{current_time:.2f}秒")
    
    return output_path


def burn_subtitles(video_path, subtitle_path, output_path):
    """使用 ffmpeg 烧录字幕"""
    
    print(f"🎬 开始烧录字幕...")
    
    # ffmpeg 命令
    cmd = [
        'ffmpeg',
        '-i', str(video_path),
        '-vf', f'ass={subtitle_path}',
        '-c:a', 'copy',
        '-y',
        str(output_path)
    ]
    
    print(f"   输入：{video_path}")
    print(f"   字幕：{subtitle_path}")
    print(f"   输出：{output_path}")
    
    # 执行 ffmpeg
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 字幕烧录完成：{output_path}")
        size_mb = Path(output_path).stat().st_size / (1024 * 1024)
        print(f"   文件大小：{size_mb:.2f} MB")
        return True
    else:
        print(f"❌ 字幕烧录失败：{result.stderr}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("用法：python add_subtitles.py <video.mp4> <audio_info.json> [output.mp4]")
        sys.exit(1)
    
    video_path = Path(sys.argv[1])
    audio_info_path = Path(sys.argv[2])
    
    if len(sys.argv) > 3:
        output_path = Path(sys.argv[3])
    else:
        output_path = video_path.parent / f"{video_path.stem}_sub.mp4"
    
    # 生成 ASS 字幕
    ass_path = video_path.parent / "subtitles.ass"
    generate_ass_subtitles(audio_info_path, ass_path)
    
    # 烧录字幕
    burn_subtitles(video_path, ass_path, output_path)
