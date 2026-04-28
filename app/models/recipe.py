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

class Recipe:
    @staticmethod
    def create(data):
        """新增一筆食譜記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO RECIPE (title, description, cooking_time_minutes, ingredients, steps) VALUES (?, ?, ?, ?, ?)',
                (data['title'], data.get('description'), data.get('cooking_time_minutes'), 
                 data.get('ingredients'), data.get('steps'))
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            print(f"建立食譜失敗: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有食譜記錄"""
        try:
            conn = get_db_connection()
            recipes = conn.execute('SELECT * FROM RECIPE').fetchall()
            conn.close()
            return recipes
        except Exception as e:
            print(f"取得食譜列表失敗: {e}")
            return []

    @staticmethod
    def get_by_id(recipe_id):
        """取得單筆食譜記錄"""
        try:
            conn = get_db_connection()
            recipe = conn.execute('SELECT * FROM RECIPE WHERE id = ?', (recipe_id,)).fetchone()
            conn.close()
            return recipe
        except Exception as e:
            print(f"取得食譜詳情失敗: {e}")
            return None

    @staticmethod
    def update(recipe_id, data):
        """更新食譜記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE RECIPE SET title = ?, description = ?, cooking_time_minutes = ?, ingredients = ?, steps = ? WHERE id = ?',
                (data['title'], data.get('description'), data.get('cooking_time_minutes'), 
                 data.get('ingredients'), data.get('steps'), recipe_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新食譜失敗: {e}")
            return False

    @staticmethod
    def delete(recipe_id):
        """刪除食譜記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM RECIPE WHERE id = ?', (recipe_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"刪除食譜失敗: {e}")
            return False
