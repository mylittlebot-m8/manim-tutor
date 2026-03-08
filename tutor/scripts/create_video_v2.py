#!/usr/bin/env python3
"""
系统化视频生成工具 v2
支持数据库管理、自动命名、状态追踪

使用方法:
    python scripts/create_video_v2.py \\
        --problem "题目文本" \\
        --title "题目标题" \\
        --category "代数" \\
        --difficulty 3
"""

import argparse
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import get_db
from scripts.generate_storyboard import generate_storyboard


def create_project(problem_text: str, title: str, category: str = "",
                   difficulty: int = 3, auto_render: bool = False):
    """
    创建系统化的题目项目
    
    Returns:
        problem_id: 生成的题目ID
    """
    
    # 1. 创建数据库记录
    db = get_db()
    problem_id = db.create_problem(title, problem_text, category, difficulty)
    
    # 获取项目信息
    problem_info = db.get_problem(problem_id)
    project_dir = Path(__file__).parent.parent / problem_info['project_dir']
    
    print(f"\n{'='*60}")
    print(f"🎬 创建题目项目: {problem_id}")
    print(f"{'='*60}")
    print(f"📁 项目目录: {project_dir}")
    print(f"📋 标题: {title}")
    print(f"🏷️  分类: {category or '未分类'}")
    print(f"⭐ 难度: {'★' * difficulty}")
    
    # 2. 创建项目目录结构
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "audio").mkdir(exist_ok=True)
    
    # 3. 生成分镜脚本
    print("\n📝 生成分镜脚本...")
    storyboard = generate_storyboard(problem_text, title=title)
    storyboard_path = project_dir / "storyboard.md"
    storyboard_path.write_text(storyboard, encoding='utf-8')
    print(f"   ✅ {storyboard_path.name}")
    
    # 更新数据库
    db.update_status(problem_id, 'generating')
    
    # 4. 复制Manim脚本模板
    print("💻 复制脚本模板...")
    template_dir = Path(__file__).parent.parent / "templates"
    script_template = template_dir / "script_with_problem.py"
    
    if script_template.exists():
        script_path = project_dir / "script.py"
        shutil.copy2(script_template, script_path)
        print(f"   ✅ {script_path.name}")
    else:
        print(f"   ⚠️  模板不存在: {script_template}")
    
    # 5. 自动渲染（可选）
    if auto_render:
        print("\n🎬 开始自动渲染...")
        render_script = Path(__file__).parent / "render_integrated.py"
        
        try:
            result = subprocess.run(
                [sys.executable, str(render_script), 
                 "-p", str(project_dir), "-q", "h"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                # 查找生成的视频
                video_file = project_dir / f"{project_dir.name}.mp4"
                if video_file.exists():
                    # 重命名为标准名称
                    final_video = project_dir / "video.mp4"
                    shutil.move(video_file, final_video)
                    
                    # 获取视频信息
                    import json
                    probe_result = subprocess.run(
                        ["ffprobe", "-v", "error", "-show_format",
                         "-of", "json", str(final_video)],
                        capture_output=True, text=True
                    )
                    video_info = json.loads(probe_result.stdout)
                    duration = float(video_info['format']['duration'])
                    size_mb = float(video_info['format']['size']) / 1024 / 1024
                    
                    # 更新数据库
                    db.update_video_info(
                        problem_id, 
                        str(final_video.relative_to(project_dir.parent.parent)),
                        duration, size_mb
                    )
                    
                    print(f"\n✅ 视频生成成功!")
                    print(f"   📹 {final_video}")
                    print(f"   ⏱️  时长: {duration:.1f}秒")
                    print(f"   📊 大小: {size_mb:.2f}MB")
                else:
                    db.update_status(problem_id, 'failed', '视频文件未找到')
            else:
                db.update_status(problem_id, 'failed', result.stderr)
                
        except subprocess.TimeoutExpired:
            db.update_status(problem_id, 'failed', '渲染超时')
        except Exception as e:
            db.update_status(problem_id, 'failed', str(e))
    
    print(f"\n{'='*60}")
    print(f"✅ 项目创建完成: {problem_id}")
    print(f"{'='*60}")
    
    if not auto_render:
        print(f"\n下一步:")
        print(f"   cd {project_dir}")
        print(f"   python ../../scripts/render_integrated.py -p . -q h")
    
    return problem_id


def list_projects(status: str = None):
    """列出所有项目"""
    db = get_db()
    problems = db.list_problems(status=status, limit=20)
    
    print(f"\n{'='*80}")
    print(f"📚 题目列表 ({len(problems)}个)")
    print(f"{'='*80}")
    print(f"{'ID':<15} {'日期':<12} {'状态':<12} {'分类':<10} {'标题':<30}")
    print("-"*80)
    
    for p in problems:
        status_icon = {
            'pending': '⏳',
            'generating': '📝',
            'rendering': '🎬',
            'completed': '✅',
            'failed': '❌'
        }.get(p['status'], '❓')
        
        title = p['title'][:28] + ".." if len(p['title']) > 30 else p['title']
        category = (p['category'] or '-')[:8]
        
        print(f"{p['problem_id']:<15} {p['date']:<12} {status_icon} {p['status']:<10} "
              f"{category:<10} {title}")
    
    print("="*80)


def main():
    parser = argparse.ArgumentParser(
        description='系统化教学视频生成工具 v2',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
    # 创建新项目
    python create_video_v2.py -p "已知x+y=10..." -t "最值问题" -c "代数" -d 3
    
    # 创建并自动渲染
    python create_video_v2.py -p "题目..." -t "标题" --auto-render
    
    # 列出所有项目
    python create_video_v2.py --list
    
    # 列出已完成的
    python create_video_v2.py --list --status completed
        '''
    )
    
    parser.add_argument('--problem', '-p', help='完整题目文本')
    parser.add_argument('--title', '-t', help='题目标题')
    parser.add_argument('--category', '-c', default='', help='分类(代数/几何/函数等)')
    parser.add_argument('--difficulty', '-d', type=int, default=3, 
                       choices=[1,2,3,4,5], help='难度1-5')
    parser.add_argument('--auto-render', action='store_true', 
                       help='自动渲染视频')
    parser.add_argument('--list', action='store_true', help='列出所有项目')
    parser.add_argument('--status', help='筛选状态(pending/completed/failed)')
    
    args = parser.parse_args()
    
    if args.list:
        list_projects(args.status)
    elif args.problem:
        create_project(
            args.problem, 
            args.title, 
            args.category, 
            args.difficulty,
            args.auto_render
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
