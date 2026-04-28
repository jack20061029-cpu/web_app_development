import sqlite3
import os

DATABASE = os.path.join('instance', 'database.db')

def get_db_connection():
    """建立資料庫連線並設定 row_factory"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"資料庫連線錯誤: {e}")
        return None

class Tag:
    @staticmethod
    def create(name):
        """新增一個標籤"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO TAG (name) VALUES (?)', (name,))
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"建立標籤失敗: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有標籤"""
        try:
            conn = get_db_connection()
            tags = conn.execute('SELECT * FROM TAG').fetchall()
            conn.close()
            return tags
        except Exception as e:
            print(f"取得標籤列表失敗: {e}")
            return []

    @staticmethod
    def get_by_id(tag_id):
        """取得單個標籤"""
        try:
            conn = get_db_connection()
            tag = conn.execute('SELECT * FROM TAG WHERE id = ?', (tag_id,)).fetchone()
            conn.close()
            return tag
        except Exception as e:
            print(f"取得標籤詳情失敗: {e}")
            return None

    @staticmethod
    def update(tag_id, name):
        """更新標籤名稱"""
        try:
            conn = get_db_connection()
            conn.execute('UPDATE TAG SET name = ? WHERE id = ?', (name, tag_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新標籤失敗: {e}")
            return False

    @staticmethod
    def delete(tag_id):
        """刪除標籤"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM TAG WHERE id = ?', (tag_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"刪除標籤失敗: {e}")
            return False
