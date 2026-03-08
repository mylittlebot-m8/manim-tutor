#!/usr/bin/env python3
"""
Manim 教学视频渲染脚本 - 远程服务集成版
完整流程: TTS生成 -> 检查代码 -> 远程渲染视频

使用方法:
    python scripts/render_integrated.py [options]

选项:
    -p, --project   项目目录 (默认: 当前目录)
    -q, --quality   渲染质量: l(ow)/m(edium)/h(igh)/k(4k) (默认: high)
    -v, --voice     TTS声音 (默认: Nofish)
    --local         使用本地渲染（如果可用）

示例:
    python scripts/render_integrated.py                    # 渲染当前项目
    python scripts/render_integrated.py -p ./my_project    # 渲染指定项目
    python scripts/render_integrated.py -q k               # 4K质量渲染
"""

import sys
import argparse
import requests
import time
import base64
import os
from pathlib import Path
# 远程服务配置
REMOTE_SERVICE_URL = "http://117.50.190.204:8000"
SERVER_IP = os.getenv("MANIM_SERVER_IP", "117.50.190.204")
SERVER_USER = os.getenv("MANIM_SERVER_USER", "ubuntu")
SERVER_PASSWORD = os.getenv("MANIM_SERVER_PASSWORD", "B3f47t0gmC21Rr86")


class IntegratedRenderPipeline:
    """集成渲染流水线 - 使用远程服务"""

    def __init__(self, project_dir='.', quality='high', voice='Nofish'):
        self.project_dir = Path(project_dir).resolve()
        self.quality = quality
        self.voice = voice
        
        # 检查必要文件
        self.storyboard_file = self.project_dir / 'storyboard.md'
        self.script_file = self.project_dir / 'script.py'
        self.audio_dir = self.project_dir / 'audio'
        
    def check_service(self):
        """检查远程服务是否可用"""
        try:
            resp = requests.get(f"{REMOTE_SERVICE_URL}/health", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                print(f"✅ 远程服务正常 (manim {data.get('manim_version', 'unknown')})")
                return True
        except Exception as e:
            print(f"❌ 无法连接到远程服务: {e}")
        return False
    
    def generate_tts(self):
        """步骤1: 生成分镜TTS音频"""
        if not self.storyboard_file.exists():
            print(f"❌ 分镜脚本不存在: {self.storyboard_file}")
            return None
        
        storyboard_content = self.storyboard_file.read_text(encoding='utf-8')
        print(f"📖 已读取分镜: {len(storyboard_content)} 字符")
        
        print("🔊 正在生成TTS音频...")
        resp = requests.post(
            f"{REMOTE_SERVICE_URL}/tts/batch",
            json={
                "storyboard_md": storyboard_content,
                "voice": self.voice
            },
            timeout=120
        )
        
        if resp.status_code != 200:
            print(f"❌ TTS生成失败: {resp.text}")
            return None
        
        result = resp.json()
        print(f"✅ TTS生成成功!")
        print(f"   🎵 音频文件: {result['count']}个")
        print(f"   ⏱️  总时长: {result['total_duration']:.2f}秒")
        
        # 下载音频文件
        self.audio_dir.mkdir(exist_ok=True)
        for f in result['files']:
            filename = f['file']
            expected_duration = f.get('duration', 0)
            print(f"   📥 下载：{filename} (预计{expected_duration}秒)...")
            
            max_retries = 3
            for attempt in range(max_retries):
                dl_resp = requests.get(f"{REMOTE_SERVICE_URL}/tts/download/{filename}", stream=True, timeout=60)
                if dl_resp.status_code == 200:
                    with open(self.audio_dir / filename, 'wb') as file:
                        for chunk in dl_resp.iter_content(chunk_size=8192):
                            file.write(chunk)
                    
                    # 验证文件大小
                    file_size = (self.audio_dir / filename).stat().st_size
                    print(f"   ✅ 下载完成：{filename} ({file_size/1024:.1f}KB)")
                    break
                else:
                    print(f"   ⚠️ 下载失败 (尝试{attempt+1}/{max_retries}): {dl_resp.status_code}")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(2)
        
        # 保存audio_info.json
        import json
        audio_info = {
            "files": result['files'],
            "total_duration": result['total_duration'],
            "count": result['count']
        }
        with open(self.audio_dir / "audio_info.json", 'w', encoding='utf-8') as f:
            json.dump(audio_info, f, ensure_ascii=False, indent=2)
        
        return result
    
    def render_video(self):
        """步骤2: 提交视频渲染任务"""
        if not self.script_file.exists():
            print(f"❌ 脚本文件不存在: {self.script_file}")
            return False
        
        script_content = self.script_file.read_text(encoding='utf-8')
        print(f"💻 脚本已就绪: {len(script_content)} 字符")
        
        # 音频已经在服务端（TTS API直接生成到服务器），不需要重新上传
        # 服务端会从 task_dir/audio/ 读取音频文件
        print(f"🎵 音频已在服务端: {self.audio_dir}")
        
        print("🎬 提交视频渲染任务...")
        # 准备音频文件（base64编码）
        audio_files = []
        if self.audio_dir.exists():
            for wav_file in sorted(self.audio_dir.glob("*.wav"))[:10]:  # 最多10个，避免太大
                try:
                    with open(wav_file, 'rb') as f:
                        content = base64.b64encode(f.read()).decode('utf-8')
                    audio_files.append({
                        "filename": wav_file.name,
                        "base64": content
                    })
                    print(f"   📎 准备音频: {wav_file.name}")
                except Exception as e:
                    print(f"   ⚠️  音频读取失败: {wav_file.name}, {e}")
        
        # 读取 storyboard.md
        storyboard_content = ""
        if self.storyboard_file.exists():
            storyboard_content = self.storyboard_file.read_text(encoding='utf-8')
            print(f"   📄 storyboard.md 长度：{len(storyboard_content)} 字符")
            print(f"   📄 第一行：{storyboard_content.split(chr(10))[0][:50]}...")
        else:
            print(f"   ⚠️  storyboard.md 不存在")
        
        print(f"🎬 提交视频渲染任务...")
        resp = requests.post(
            f"{REMOTE_SERVICE_URL}/render",
            json={
                "project_name": self.project_dir.name,
                "script_content": script_content,
                "storyboard_md": storyboard_content,  # 上传 storyboard
                "audio_files": audio_files,
                "quality": self.quality,
                "scene_name": "ParabolaProblem"  # 或从脚本中检测
            },
            timeout=300
        )
        
        if resp.status_code != 200:
            print(f"❌ 渲染提交失败: {resp.text}")
            return False
        
        task = resp.json()
        task_id = task["task_id"]
        print(f"✅ 渲染任务已提交: {task_id}")
        
        # 等待渲染完成
        print("⏳ 等待渲染完成...")
        while True:
            status_resp = requests.get(f"{REMOTE_SERVICE_URL}/task/{task_id}", timeout=60)
            if status_resp.status_code != 200:
                print("❌ 查询状态失败")
                return False
            
            status = status_resp.json()
            current = status["status"]
            progress = status["progress"]
            message = status["message"]
            
            print(f"   [{current}] {progress}% - {message}")
            
            if current == "completed":
                print(f"\n✅ 渲染完成!")
                output_file = status.get("output_file")
                print(f"📁 输出文件: {output_file}")
                
                # 下载视频
                print("⬇️  下载视频...")
                dl_resp = requests.get(f"{REMOTE_SERVICE_URL}/download/{task_id}", stream=True)
                if dl_resp.status_code == 200:
                    video_path = self.project_dir / f"{self.project_dir.name}.mp4"
                    with open(video_path, 'wb') as f:
                        for chunk in dl_resp.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"✅ 视频已保存: {video_path}")
                    
                    # 显示文件大小
                    size_mb = video_path.stat().st_size / (1024 * 1024)
                    print(f"📊 文件大小: {size_mb:.2f} MB")
                    return True
                else:
                    print(f"❌ 下载失败: {dl_resp.status_code}")
                    return False
            
            elif current == "failed":
                print(f"\n❌ 渲染失败: {status.get('error_log', '未知错误')}")
                return False
            
            time.sleep(5)
    
    def run(self):
        """运行完整流程"""
        print("=" * 60)
        print("🎬 Manim 远程渲染流水线")
        print("=" * 60)
        print(f"项目目录: {self.project_dir}")
        print(f"服务质量: {self.quality}")
        print(f"TTS声音: {self.voice}")
        print("=" * 60 + "\n")
        
        # 检查服务
        if not self.check_service():
            return False
        
        # 步骤1: TTS生成
        tts_result = self.generate_tts()
        if not tts_result:
            return False
        
        # 步骤2: 视频渲染
        success = self.render_video()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 全部完成!")
        else:
            print("❌ 流程失败")
        print("=" * 60)
        
        return success


def main():
    parser = argparse.ArgumentParser(
        description='Manim 远程渲染流水线',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-p', '--project',
        default='.',
        help='项目目录 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '-q', '--quality',
        default='high',
        choices=['l', 'low', 'm', 'medium', 'h', 'high', 'k', '4k'],
        help='渲染质量'
    )
    
    parser.add_argument(
        '-v', '--voice',
        default='Nofish',
        help='TTS声音 (默认: Nofish)'
    )
    
    args = parser.parse_args()
    
    pipeline = IntegratedRenderPipeline(
        project_dir=args.project,
        quality=args.quality,
        voice=args.voice
    )
    
    success = pipeline.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
