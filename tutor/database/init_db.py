#!/usr/bin/env python3
"""
初始化题目数据库
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "problems.db"


def init_database():
    """创建数据库和表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建题目表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,        -- UUID主键 (如: a1b2c3d4)
            problem_id TEXT UNIQUE NOT NULL,  -- 人类可读ID: YYYYMMDD_序号
            date TEXT NOT NULL,               -- 创建日期
            title TEXT NOT NULL,              -- 题目标题
            problem_text TEXT NOT NULL,       -- 完整题目文本
            category TEXT,                    -- 分类: 代数/几何/函数/应用题等
            difficulty INTEGER DEFAULT 3,     -- 难度 1-5
            local_project_dir TEXT,           -- 本地项目目录路径
            server_project_dir TEXT,          -- 服务器项目目录路径
            server_tts_dir TEXT,              -- 服务器TTS音频目录
            storyboard_path TEXT,             -- 分镜脚本路径
            script_path TEXT,                 -- Manim脚本路径
            video_path TEXT,                  -- 视频文件路径
            audio_count INTEGER DEFAULT 0,    -- 音频文件数量
            duration_seconds REAL,            -- 视频时长(秒)
            file_size_mb REAL,                -- 文件大小(MB)
            status TEXT DEFAULT 'pending',    -- pending/generating/rendering/completed/failed
            error_message TEXT,               -- 错误信息
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON problems(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON problems(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON problems(status)')
    
    conn.commit()
    conn.close()
    print(f"✅ 数据库初始化完成: {DB_PATH}")


if __name__ == "__main__":
    init_database()
