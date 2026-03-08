#!/usr/bin/env python3
"""
本地TTS生成 + 上传到服务端渲染
确保TTS内容正确
"""

import sys
import requests
import time
import base64
import json
from pathlib import Path

# 服务端配置
REMOTE_SERVICE_URL = "http://117.50.190.204:8000"


def generate_tts_locally(storyboard_content: str, voice: str = "Nofish"):
    """本地生成TTS"""
    print("🔊 本地生成TTS...")
    
    resp = requests.post(
        f"{REMOTE_SERVICE_URL}/tts/batch",
        json={
            "storyboard_md": storyboard_content,
            "voice": voice
        },
        timeout=120
    )
    
    if resp.status_code != 200:
        print(f"❌ TTS生成失败：{resp.text}")
        return None
    
    result = resp.json()
    print(f"✅ TTS生成成功！{result['count']}个文件，总时长{result['total_duration']:.2f}秒")
    
    return result


def download_audio_files(audio_dir: Path, files: list):
    """下载音频文件"""
    audio_dir.mkdir(exist_ok=True)
    
    for f in files:
        filename = f['file']
        dl_resp = requests.get(
            f"{REMOTE_SERVICE_URL}/tts/download/{filename}",
            stream=True,
            timeout=60
        )
        
        if dl_resp.status_code == 200:
            with open(audio_dir / filename, 'wb') as file:
                for chunk in dl_resp.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"   ✅ 下载：{filename}")
        else:
            print(f"   ❌ 下载失败：{filename}")
    
    print(f"✅ 音频下载完成")


def render_video(project_dir: Path, audio_dir: Path, script_file: Path, quality: str = "h"):
    """上传音频并渲染视频"""
    script_content = script_file.read_text(encoding='utf-8')
    
    # 准备音频文件（base64编码）
    audio_files = []
    for wav_file in sorted(audio_dir.glob("*.wav")):
        with open(wav_file, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        audio_files.append({
            "filename": wav_file.name,
            "base64": content
        })
    
    print(f"🎬 提交视频渲染任务... ({len(audio_files)}个音频文件)")
    
    resp = requests.post(
        f"{REMOTE_SERVICE_URL}/render",
        json={
            "project_name": project_dir.name,
            "script_content": script_content,
            "audio_files": audio_files,
            "quality": quality,
            "scene_name": "TeachingScene"
        },
        timeout=300
    )
    
    if resp.status_code != 200:
        print(f"❌ 渲染提交失败：{resp.text}")
        return False
    
    task_id = resp.json()['task_id']
    print(f"✅ 渲染任务已提交：{task_id}")
    
    # 轮询状态
    print("⏳ 等待渲染完成...")
    while True:
        status_resp = requests.get(f"{REMOTE_SERVICE_URL}/task/{task_id}", timeout=60)
        status = status_resp.json()
        
        if status['status'] == 'completed':
            print(f"✅ 渲染完成!")
            break
        elif status['status'] == 'failed':
            print(f"❌ 渲染失败：{status.get('error_log', '未知错误')}")
            return False
        
        time.sleep(5)
        print(f"   [rendering] {status.get('progress', 0)}% - {status.get('message', '渲染中...')}")
    
    # 下载视频
    video_url = f"{REMOTE_SERVICE_URL}/download/{task_id}"
    dl_resp = requests.get(video_url, stream=True, timeout=300)
    
    output_file = project_dir / f"{project_dir.name}.mp4"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'wb') as f:
        for chunk in dl_resp.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"✅ 视频已保存：{output_file}")
    print(f"   文件大小：{output_file.stat().st_size / 1024 / 1024:.2f} MB")
    return True


def main():
    if len(sys.argv) < 2:
        print("用法：python render_local_tts.py <项目目录> [质量]")
        sys.exit(1)
    
    project_dir = Path(sys.argv[1])
    quality = sys.argv[2] if len(sys.argv) > 2 else "h"
    
    if not project_dir.exists():
        print(f"❌ 项目目录不存在：{project_dir}")
        sys.exit(1)
    
    storyboard_file = project_dir / "storyboard.md"
    script_file = project_dir / "script.py"
    audio_dir = project_dir / "audio"
    
    if not storyboard_file.exists():
        print(f"❌ 分镜脚本不存在：{storyboard_file}")
        sys.exit(1)
    
    if not script_file.exists():
        print(f"❌ 脚本文件不存在：{script_file}")
        sys.exit(1)
    
    # 1. 本地生成TTS
    storyboard_content = storyboard_file.read_text(encoding='utf-8')
    tts_result = generate_tts_locally(storyboard_content)
    
    if not tts_result:
        sys.exit(1)
    
    # 2. 下载音频文件
    download_audio_files(audio_dir, tts_result['files'])
    
    # 3. 保存audio_info.json
    with open(audio_dir / "audio_info.json", 'w', encoding='utf-8') as f:
        json.dump(tts_result, f, ensure_ascii=False, indent=2)
    
    # 4. 渲染视频
    success = render_video(project_dir, audio_dir, script_file, quality)
    
    if success:
        print("\n🎉 全部完成!")
    else:
        print("\n❌ 流程失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
