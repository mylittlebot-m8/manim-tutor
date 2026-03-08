#!/usr/bin/env python3
"""
Manim 教学视频渲染脚本 - 远程服务版
通过FastAPI接口调用远程Manim渲染服务

使用方法:
    python scripts/render_remote.py [options]

环境变量:
    MANIM_SERVICE_URL=http://117.50.91.193:8000
    MANIM_API_KEY=your-api-key (可选)

示例:
    python scripts/render_remote.py                    # 默认渲染当前项目
    python scripts/render_remote.py -p my_project      # 指定项目目录
    python scripts/render_remote.py -q k               # 4K质量渲染
"""

import sys
import argparse
import os
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from tutor_client import ManimRendererClient
except ImportError:
    print("❌ 请先安装依赖: pip install requests")
    sys.exit(1)


class RemoteRenderPipeline:
    """远程渲染流水线"""

    def __init__(self, project_dir='.', quality='high', voice='xiaoxiao'):
        self.project_dir = Path(project_dir).resolve()
        self.quality = quality
        self.voice = voice

        # 从环境变量读取服务配置
        self.service_url = os.getenv('MANIM_SERVICE_URL', 'http://117.50.91.193:8000')
        self.api_key = os.getenv('MANIM_API_KEY')

        # 初始化客户端
        self.client = ManimRendererClient(
            base_url=self.service_url,
            api_key=self.api_key
        )

        # 检查必要文件
        self.storyboard_file = self.project_dir / 'storyboard.md'
        self.script_file = self.project_dir / 'script.py'

    def check_service(self):
        """检查远程服务是否可用"""
        print("🔍 检查远程服务...")
        if not self.client.health_check():
            print(f"❌ 无法连接到Manim渲染服务: {self.service_url}")
            print("   请确保:")
            print("   1. 服务已启动")
            print("   2. 网络连接正常")
            print("   3. MANIM_SERVICE_URL环境变量设置正确")
            return False
        print(f"✅ 已连接到服务: {self.service_url}")
        return True

    def read_storyboard(self):
        """读取分镜脚本"""
        if not self.storyboard_file.exists():
            print(f"❌ 分镜脚本不存在: {self.storyboard_file}")
            print("   请先创建分镜脚本: storyboard.md")
            return None

        content = self.storyboard_file.read_text(encoding='utf-8')
        print(f"✅ 已读取分镜脚本: {len(content)} 字符")
        return content

    def run(self):
        """运行完整渲染流程"""
        print("\n" + "=" * 60)
        print("🎬 Manim 远程视频渲染流水线")
        print("=" * 60)
        print(f"项目目录: {self.project_dir}")
        print(f"服务地址: {self.service_url}")
        print(f"渲染质量: {self.quality}")
        print(f"TTS声音: {self.voice}")
        print("=" * 60 + "\n")

        # 步骤1: 检查服务
        if not self.check_service():
            return False

        # 步骤2: 读取分镜
        storyboard = self.read_storyboard()
        if not storyboard:
            return False

        # 步骤3: 执行完整工作流
        try:
            project_name = self.project_dir.name
            output_file = self.project_dir / f"{project_name}.mp4"

            video_path = self.client.full_workflow(
                name=project_name,
                storyboard_md=storyboard,
                description=f"Project from {self.project_dir}",
                voice=self.voice,
                quality=self.quality,
                output_path=str(output_file)
            )

            print("\n" + "=" * 60)
            print("✅ 渲染完成！")
            print("=" * 60)
            print(f"视频文件: {video_path}")
            return True

        except Exception as e:
            print(f"\n❌ 渲染失败: {e}")
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Manim 远程视频渲染流水线',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
环境变量:
    MANIM_SERVICE_URL   远程服务地址 (默认: http://117.50.91.193:8000)
    MANIM_API_KEY       API密钥 (如果需要认证)

示例:
    python scripts/render_remote.py                    # 渲染当前目录
    python scripts/render_remote.py -p ./my_project    # 渲染指定项目
    python scripts/render_remote.py -q k               # 4K质量
    MANIM_SERVICE_URL=http://other-server:8000 python scripts/render_remote.py
        '''
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
        help='渲染质量: l/low(480p), m/medium(720p), h/high(1080p), k/4k(2160p)'
    )

    parser.add_argument(
        '-v', '--voice',
        default='xiaoxiao',
        choices=['xiaoxiao', 'xiaoyi', 'yunjian', 'yunyang'],
        help='TTS声音 (默认: xiaoxiao)'
    )

    args = parser.parse_args()

    # 创建流水线
    pipeline = RemoteRenderPipeline(
        project_dir=args.project,
        quality=args.quality,
        voice=args.voice
    )

    # 运行
    success = pipeline.run()

    # 退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
