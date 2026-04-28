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

class RecipeTag:
    @staticmethod
    def add_tag_to_recipe(recipe_id, tag_id):
        """將標籤關聯至食譜"""
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO RECIPE_TAG (recipe_id, tag_id) VALUES (?, ?)', (recipe_id, tag_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"關聯標籤失敗: {e}")
            return False

    @staticmethod
    def get_tags_for_recipe(recipe_id):
        """取得特定食譜的所有標籤"""
        try:
            conn = get_db_connection()
            tags = conn.execute('''
                SELECT TAG.* FROM TAG 
                JOIN RECIPE_TAG ON TAG.id = RECIPE_TAG.tag_id 
                WHERE RECIPE_TAG.recipe_id = ?
            ''', (recipe_id,)).fetchall()
            conn.close()
            return tags
        except Exception as e:
            print(f"取得食譜標籤失敗: {e}")
            return []

    @staticmethod
    def remove_all_tags_from_recipe(recipe_id):
        """移除食譜的所有標籤關聯"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM RECIPE_TAG WHERE recipe_id = ?', (recipe_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"移除標籤關聯失敗: {e}")
            return False
