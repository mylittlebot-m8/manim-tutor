#!/usr/bin/env python3
"""
生成 ASS 字幕文件
从 audio_info.json 读取音频时长和文本，生成同步字幕
"""

import json
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


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python generate_subtitles.py <audio_info.json> [output.ass]")
        sys.exit(1)
    
    audio_info_path = Path(sys.argv[1])
    
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
    else:
        output_path = audio_info_path.parent / "subtitles.ass"
    
    generate_ass_subtitles(audio_info_path, output_path)
