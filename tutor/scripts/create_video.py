#!/usr/bin/env python3
"""
一键生成教学视频 - 完整流程
从题目文本 → 分镜 → TTS → 视频

使用方法:
    python scripts/create_video.py --problem "题目文本" --title "标题"
    
示例:
    python scripts/create_video.py \\
        --problem "已知...求..." \\
        --title "应用题解析" \\
        --output ./my_video
"""

import argparse
import sys
import shutil
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_storyboard import generate_storyboard


def create_project(project_dir: Path, problem_text: str, title: str):
    """创建项目结构和文件"""
    
    print(f"📁 创建项目: {project_dir}")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 生成分镜脚本
    print("📝 生成分镜脚本...")
    storyboard = generate_storyboard(problem_text, title=title)
    storyboard_path = project_dir / "storyboard.md"
    storyboard_path.write_text(storyboard, encoding='utf-8')
    print(f"   ✅ {storyboard_path}")
    
    # 2. 复制Manim脚本模板
    print("💻 复制脚本模板...")
    template_dir = Path(__file__).parent.parent / "templates"
    script_template = template_dir / "script_with_problem.py"
    
    if script_template.exists():
        script_path = project_dir / "script.py"
        shutil.copy2(script_template, script_path)
        print(f"   ✅ {script_path}")
    else:
        print(f"   ⚠️ 模板不存在: {script_template}")
    
    # 3. 创建音频目录
    audio_dir = project_dir / "audio"
    audio_dir.mkdir(exist_ok=True)
    print(f"   ✅ {audio_dir}/")
    
    print(f"\n✅ 项目创建完成!")
    print(f"   位置: {project_dir}")
    print(f"\n下一步:")
    print(f"   cd {project_dir}")
    print(f"   python ../../scripts/render_integrated.py -p . -q h")


def main():
    parser = argparse.ArgumentParser(
        description='一键生成教学视频',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
    python create_video.py -p "已知x+y=10，求x*y最大值" -t "最值问题"
    python create_video.py -p "抛物线y=x²..." -t "抛物线综合题" -o ./parabola
        '''
    )
    
    parser.add_argument(
        '--problem', '-p',
        required=True,
        help='完整题目文本（用引号包裹）'
    )
    
    parser.add_argument(
        '--title', '-t',
        default='',
        help='视频标题（可选，自动提取）'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='./video_project',
        help='输出目录（默认: ./video_project）'
    )
    
    args = parser.parse_args()
    
    # 创建项目
    project_dir = Path(args.output)
    create_project(project_dir, args.problem, args.title)


if __name__ == "__main__":
    main()
