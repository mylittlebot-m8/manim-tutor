#!/usr/bin/env python3
"""
Tutor Skill - Manim渲染服务客户端

用于在本地skill中调用远程Manim渲染服务
"""

import requests
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any


class ManimRendererClient:
    """Manim渲染服务客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def health_check(self) -> bool:
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def create_project(self, name: str, description: str = "") -> Dict[str, Any]:
        """创建新项目"""
        response = requests.post(
            f"{self.base_url}/api/v1/projects",
            headers=self.headers,
            json={"name": name, "description": description}
        )
        response.raise_for_status()
        return response.json()
    
    def upload_storyboard(self, project_id: str, storyboard_md: str) -> Dict[str, Any]:
        """上传分镜脚本（Markdown格式）"""
        response = requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/storyboard",
            headers=self.headers,
            json={"content": storyboard_md}
        )
        response.raise_for_status()
        return response.json()
    
    def generate_audio(self, project_id: str, voice: str = "xiaoxiao") -> Dict[str, Any]:
        """生成TTS音频"""
        response = requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/audio",
            headers=self.headers,
            json={"voice": voice}
        )
        response.raise_for_status()
        return response.json()
    
    def validate_audio(self, project_id: str) -> Dict[str, Any]:
        """验证音频并更新分镜时长"""
        response = requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/validate",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def generate_script(self, project_id: str) -> Dict[str, Any]:
        """生成Manim代码脚手架"""
        response = requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/script",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def render_video(
        self,
        project_id: str,
        quality: str = "h",
        scene_name: str = "MathScene"
    ) -> Dict[str, Any]:
        """提交视频渲染任务"""
        response = requests.post(
            f"{self.base_url}/api/v1/projects/{project_id}/render",
            headers=self.headers,
            json={
                "quality": quality,
                "scene_name": scene_name
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """获取项目状态和详情"""
        response = requests.get(
            f"{self.base_url}/api/v1/projects/{project_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def download_video(self, project_id: str, output_path: str) -> bool:
        """下载生成的视频"""
        response = requests.get(
            f"{self.base_url}/api/v1/projects/{project_id}/download",
            headers=self.headers,
            stream=True
        )
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False
    
    def wait_for_completion(
        self,
        project_id: str,
        poll_interval: float = 5.0,
        timeout: float = 600.0
    ) -> Dict[str, Any]:
        """等待项目完成，轮询状态"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_project(project_id)
            
            if status["status"] == "completed":
                return status
            elif status["status"] == "failed":
                raise RuntimeError(f"项目失败: {status.get('error', '未知错误')}")
            
            time.sleep(poll_interval)
        
        raise TimeoutError("等待超时")
    
    def full_workflow(
        self,
        name: str,
        storyboard_md: str,
        description: str = "",
        voice: str = "xiaoxiao",
        quality: str = "h",
        output_path: Optional[str] = None
    ) -> str:
        """
        执行完整工作流，返回视频文件路径
        
        Args:
            name: 项目名称
            storyboard_md: 分镜脚本（Markdown格式）
            description: 项目描述
            voice: TTS声音
            quality: 视频质量 (l/m/h/k)
            output_path: 输出文件路径（可选）
        
        Returns:
            视频文件路径
        """
        print(f"🚀 开始制作教学视频: {name}")
        
        # 1. 创建项目
        print("📁 创建项目...")
        project = self.create_project(name, description)
        project_id = project["project_id"]
        print(f"   项目ID: {project_id}")
        
        # 2. 上传分镜
        print("📝 上传分镜脚本...")
        self.upload_storyboard(project_id, storyboard_md)
        
        # 3. 生成音频
        print("🔊 生成配音...")
        self.generate_audio(project_id, voice)
        
        # 等待音频生成
        print("   等待音频生成...")
        while True:
            status = self.get_project(project_id)
            if status["status"] in ["audio_ready", "script_ready", "completed"]:
                break
            elif status["status"] == "failed":
                raise RuntimeError("音频生成失败")
            time.sleep(2)
        print("   ✅ 音频生成完成")
        
        # 4. 验证音频
        print("✓ 验证音频...")
        result = self.validate_audio(project_id)
        print(f"   总时长: {result.get('total_duration', 0):.1f}秒")
        
        # 5. 生成代码
        print("💻 生成动画代码...")
        self.generate_script(project_id)
        
        # 6. 渲染视频
        print("🎬 渲染视频...")
        self.render_video(project_id, quality)
        
        # 等待渲染完成
        print("   渲染中（可能需要几分钟）...")
        final_status = self.wait_for_completion(project_id)
        print("   ✅ 渲染完成")
        
        # 7. 下载视频
        if output_path is None:
            output_path = f"./{name.replace(' ', '_')}.mp4"
        
        print(f"⬇️  下载视频到: {output_path}")
        if self.download_video(project_id, output_path):
            print("✅ 视频下载成功！")
            return output_path
        else:
            raise RuntimeError("视频下载失败")


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 初始化客户端
    client = ManimRendererClient(
        base_url="http://your-server-ip:8000",
        # api_key="your-api-key"  # 如果需要认证
    )
    
    # 检查服务
    if not client.health_check():
        print("❌ 无法连接到Manim渲染服务")
        exit(1)
    
    print("✅ 已连接到Manim渲染服务")
    
    # 定义分镜脚本
    storyboard = '''# 分镜脚本 - 勾股定理证明

### 第1幕：开场
**画面**: 标题显示
**字幕**: "勾股定理"
**读白**: "今天我们来学习勾股定理，这是几何学中最重要的定理之一。"

### 第2幕：展示三角形
**画面**: 直角三角形ABC，角C为直角
**字幕**: "直角三角形"
**读白**: "考虑一个直角三角形ABC，其中角C是直角。"

### 第3幕：公式
**画面**: 显示 a² + b² = c²
**字幕**: "a² + b² = c²"
**读白**: "勾股定理告诉我们：两条直角边的平方和等于斜边的平方。"
'''
    
    # 执行完整工作流
    try:
        video_path = client.full_workflow(
            name="勾股定理证明",
            storyboard_md=storyboard,
            description="用图形方式证明勾股定理",
            voice="xiaoxiao",
            quality="h",
            output_path="./pythagorean_theorem.mp4"
        )
        print(f"\n🎉 视频已生成: {video_path}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
