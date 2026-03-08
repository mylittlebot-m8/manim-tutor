#!/usr/bin/env python3
"""
Manim渲染 - 直接调用服务端API
使用服务端提供的简化API接口
"""

import requests
import json
import time
import sys
from pathlib import Path

SERVICE_URL = "http://117.50.91.193:8000"


def submit_render(storyboard_path: str, output_name: str = "video"):
    """提交渲染任务"""
    
    # 读取分镜脚本
    storyboard = Path(storyboard_path).read_text(encoding='utf-8')
    
    # 构建请求
    files = {
        'storyboard': ('storyboard.md', storyboard, 'text/markdown')
    }
    data = {
        'project_name': output_name,
        'quality': 'h',
        'voice': 'xiaoxiao'
    }
    
    print("🚀 提交渲染任务...")
    response = requests.post(
        f"{SERVICE_URL}/render",
        files=files,
        data=data
    )
    
    if response.status_code != 200:
        print(f"❌ 提交失败: {response.text}")
        return None
    
    result = response.json()
    task_id = result.get('task_id')
    print(f"✅ 任务已提交: {task_id}")
    
    return task_id


def wait_for_completion(task_id: str, poll_interval: int = 5):
    """等待渲染完成"""
    print("⏳ 等待渲染完成...")
    
    while True:
        response = requests.get(f"{SERVICE_URL}/task/{task_id}")
        status = response.json()
        
        current_status = status.get('status')
        progress = status.get('progress', 0)
        message = status.get('message', '')
        
        print(f"   [{current_status}] {progress:.0%} - {message}")
        
        if current_status == 'completed':
            print("✅ 渲染完成！")
            return status
        elif current_status == 'failed':
            print(f"❌ 渲染失败: {status.get('error', '未知错误')}")
            return None
        
        time.sleep(poll_interval)


def download_video(task_id: str, output_path: str):
    """下载视频"""
    print(f"⬇️  下载视频到: {output_path}")
    
    response = requests.get(
        f"{SERVICE_URL}/download/{task_id}",
        stream=True
    )
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("✅ 下载完成！")
        return True
    else:
        print(f"❌ 下载失败: {response.text}")
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python render_direct.py <storyboard.md> [output_name]")
        sys.exit(1)
    
    storyboard_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else "video"
    
    # 检查服务
    print("🔍 检查服务...")
    try:
        response = requests.get(f"{SERVICE_URL}/health", timeout=5)
        health = response.json()
        print(f"✅ 服务正常 (manim {health.get('manim_version', 'unknown')})")
    except Exception as e:
        print(f"❌ 无法连接服务: {e}")
        sys.exit(1)
    
    # 提交任务
    task_id = submit_render(storyboard_path, output_name)
    if not task_id:
        sys.exit(1)
    
    # 等待完成
    status = wait_for_completion(task_id)
    if not status:
        sys.exit(1)
    
    # 下载视频
    output_file = f"{output_name}.mp4"
    if download_video(task_id, output_file):
        print(f"\n🎉 视频已生成: {output_file}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
