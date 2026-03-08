#!/usr/bin/env python3
"""
题目数据库管理模块
"""

import sqlite3
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

DB_PATH = Path(__file__).parent / "problems.db"
SERVER_BASE_DIR = "/home/ubuntu/math/projects"


class ProblemDB:
    """题目数据库管理类"""
    
    def __init__(self):
        self.db_path = DB_PATH
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def generate_uuid(self) -> str:
        """生成UUID (8位短UUID)"""
        return uuid.uuid4().hex[:8]
    
    def generate_problem_id(self) -> str:
        """生成人类可读的题目ID: YYYYMMDD_序号"""
        today = datetime.now().strftime("%Y%m%d")
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 查询今天已有的题目数量
        cursor.execute(
            "SELECT COUNT(*) FROM problems WHERE date = ?",
            (datetime.now().strftime("%Y-%m-%d"),)
        )
        count = cursor.fetchone()[0]
        conn.close()
        
        # 生成ID: 20260303_001
        return f"{today}_{count + 1:03d}"
    
    def create_problem_with_uuid(self, title: str, problem_text: str, 
                                  category: str = "", difficulty: int = 3) -> dict:
        """
        创建新题目记录（使用UUID目录）
        
        Returns:
            dict: {uuid, problem_id, project_dir, server_dir}
        """
        problem_uuid = self.generate_uuid()
        problem_id = self.generate_problem_id()
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # 本地项目目录：projects/{uuid}_{title}
        safe_title = "".join(c if c.isalnum() or c in '-_' else "_" for c in title[:20])
        local_dir = f"projects/{problem_uuid}_{safe_title}"
        
        # 服务器项目目录：/home/ubuntu/math/projects/{uuid}
        server_dir = f"{SERVER_BASE_DIR}/{problem_uuid}"
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO problems 
            (uuid, problem_id, date, title, problem_text, category, difficulty, 
             local_project_dir, server_project_dir, server_tts_dir, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        ''', (problem_uuid, problem_id, date_str, title, problem_text, category, 
              difficulty, local_dir, server_dir, f"{server_dir}/audio"))
        
        conn.commit()
        conn.close()
        
        return {
            "uuid": problem_uuid,
            "problem_id": problem_id,
            "local_dir": local_dir,
            "server_dir": server_dir,
            "server_tts_dir": f"{server_dir}/audio"
        }
    
    def create_problem(self, title: str, problem_text: str, 
                       category: str = "", difficulty: int = 3) -> str:
        """
        创建新题目记录
        
        Returns:
            problem_id: 生成的题目ID
        """
        problem_id = self.generate_problem_id()
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # 项目目录: projects/YYYYMMDD_序号_标题
        safe_title = "".join(c if c.isalnum() else "_" for c in title[:20])
        project_dir = f"projects/{problem_id}_{safe_title}"
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO problems 
            (problem_id, date, title, problem_text, category, difficulty, 
             project_dir, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
        ''', (problem_id, date_str, title, problem_text, category, 
              difficulty, project_dir))
        
        conn.commit()
        conn.close()
        
        print(f"✅ 题目已创建: {problem_id}")
        return problem_id
    
    def update_status(self, problem_id: str, status: str, 
                      error_message: str = None):
        """更新题目状态"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE problems 
            SET status = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP
            WHERE problem_id = ?
        ''', (status, error_message, problem_id))
        
        conn.commit()
        conn.close()
    
    def update_video_info(self, problem_id: str, video_path: str,
                          duration: float, file_size: float):
        """更新视频信息"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE problems 
            SET video_path = ?, duration_seconds = ?, file_size_mb = ?,
                status = 'completed', updated_at = CURRENT_TIMESTAMP
            WHERE problem_id = ?
        ''', (video_path, duration, file_size, problem_id))
        
        conn.commit()
        conn.close()
    
    def get_problem(self, problem_id: str) -> Optional[Dict]:
        """获取单个题目信息"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM problems WHERE problem_id = ?
        ''', (problem_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def list_problems(self, status: str = None, category: str = None,
                      limit: int = 50) -> List[Dict]:
        """列出题目"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM problems WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return result
    
    def search_problems(self, keyword: str) -> List[Dict]:
        """搜索题目"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM problems 
            WHERE title LIKE ? OR problem_text LIKE ?
            ORDER BY created_at DESC
        ''', (f"%{keyword}%", f"%{keyword}%"))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return result


# 便捷函数
def get_db() -> ProblemDB:
    """获取数据库实例"""
    return ProblemDB()


if __name__ == "__main__":
    # 测试
    db = get_db()
    
    # 列出所有题目
    problems = db.list_problems()
    print(f"\n共有 {len(problems)} 个题目")
    
    for p in problems[:5]:
        print(f"  - {p['problem_id']}: {p['title']} [{p['status']}]")
