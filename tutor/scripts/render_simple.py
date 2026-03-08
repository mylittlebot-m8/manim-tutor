#!/usr/bin/env python3
"""
简化版渲染脚本 - 直接使用服务端API
"""

import requests
import sys
import time
from pathlib import Path

BASE_URL = "http://117.50.91.193:8000"


def main():
    # 读取分镜文件
    storyboard_file = Path("test_parabola/storyboard.md")
    if not storyboard_file.exists():
        print(f"❌ 找不到分镜文件: {storyboard_file}")
        sys.exit(1)
    
    storyboard_content = storyboard_file.read_text(encoding='utf-8')
    print(f"✅ 已读取分镜文件: {len(storyboard_content)} 字符")
    
    # 检查服务
    print("🔍 检查服务...")
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if resp.status_code != 200:
        print("❌ 服务不可用")
        sys.exit(1)
    health = resp.json()
    print(f"✅ 服务正常 (manim {health.get('manim_version', 'unknown')})")
    
    # 读取Manim脚本
    script_file = Path("test_parabola/script.py")
    if not script_file.exists():
        print(f"❌ 找不到脚本文件: {script_file}")
        sys.exit(1)
    
    script_content = script_file.read_text(encoding='utf-8')
    print(f"✅ 已读取脚本文件: {len(script_content)} 字符")
    
    # 提交渲染任务 - 使用JSON格式
    print("🚀 提交渲染任务...")
    payload = {
        "project_name": "抛物线问题讲解",
        "quality": "h",
        "scene_name": "ParabolaScene",
        "script_content": script_content
    }
    
    resp = requests.post(
        f"{BASE_URL}/render",
        json=payload,
        timeout=30
    )
    
    if resp.status_code != 200:
        print(f"❌ 提交失败: {resp.text}")
        sys.exit(1)
    
    result = resp.json()
    task_id = result.get("task_id")
    print(f"✅ 任务已提交: {task_id}")
    
    # 轮询等待完成
    print("⏳ 等待渲染完成...")
    while True:
        resp = requests.get(f"{BASE_URL}/task/{task_id}", timeout=10)
        if resp.status_code != 200:
            print(f"❌ 查询状态失败")
            break
        
        status = resp.json()
        current_status = status.get("status")
        progress = status.get("progress", 0)
        message = status.get("message", "")
        
        print(f"   [{current_status}] {progress:.0%} - {message}")
        
        if current_status == "completed":
            print("\n✅ 渲染完成!")
            output_file = status.get("output_file")
            if output_file:
                print(f"📁 输出文件: {output_file}")
                
                # 下载视频
                print("⬇️  下载视频...")
                dl_resp = requests.get(f"{BASE_URL}/download/{task_id}", stream=True)
                if dl_resp.status_code == 200:
                    output_path = f"test_parabola/video_{task_id}.mp4"
                    with open(output_path, 'wb') as f:
                        for chunk in dl_resp.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"✅ 视频已保存: {output_path}")
                else:
                    print(f"❌ 下载失败: {dl_resp.status_code}")
            break
        elif current_status == "failed":
            print(f"\n❌ 渲染失败: {status.get('error_log', '未知错误')}")
            break
        
        time.sleep(5)


if __name__ == "__main__":
    main()
