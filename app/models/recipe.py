# Recipe model with CRUD operations using SQLite
import json
from typing import List, Dict, Any
from sqlite3 import Connection

class Recipe:
    TABLE_NAME = "RECIPE"

    def __init__(self, id: int = None, title: str = "", description: str = "", cooking_time_minutes: int = 0,
                 ingredients: List[Dict[str, Any]] = None, steps: List[str] = None):
        self.id = id
        self.title = title
        self.description = description
        self.cooking_time_minutes = cooking_time_minutes
        self.ingredients = ingredients or []
        self.steps = steps or []

    @staticmethod
    def create_table(conn: Connection):
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {Recipe.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                cooking_time_minutes INTEGER,
                ingredients TEXT,
                steps TEXT
            );
            """
        )
        conn.commit()

    def save(self, conn: Connection):
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                f"INSERT INTO {Recipe.TABLE_NAME} (title, description, cooking_time_minutes, ingredients, steps) VALUES (?,?,?,?,?)",
                (self.title, self.description, self.cooking_time_minutes,
                 json.dumps(self.ingredients), json.dumps(self.steps))
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                f"UPDATE {Recipe.TABLE_NAME} SET title = ?, description = ?, cooking_time_minutes = ?, ingredients = ?, steps = ? WHERE id = ?",
                (self.title, self.description, self.cooking_time_minutes,
                 json.dumps(self.ingredients), json.dumps(self.steps), self.id)
            )
        conn.commit()

    @staticmethod
    def get_all(conn: Connection) -> List['Recipe']:
        rows = conn.execute(f"SELECT * FROM {Recipe.TABLE_NAME}").fetchall()
        return [Recipe._from_row(row) for row in rows]

    @staticmethod
    def get_by_id(conn: Connection, recipe_id: int) -> 'Recipe':
        row = conn.execute(f"SELECT * FROM {Recipe.TABLE_NAME} WHERE id = ?", (recipe_id,)).fetchone()
        return Recipe._from_row(row) if row else None

    @staticmethod
    def _from_row(row):
        return Recipe(
            id=row[0],
            title=row[1],
            description=row[2],
            cooking_time_minutes=row[3],
            ingredients=json.loads(row[4] or "[]"),
            steps=json.loads(row[5] or "[]")
        )

    def delete(self, conn: Connection):
        if self.id:
            conn.execute(f"DELETE FROM {Recipe.TABLE_NAME} WHERE id = ?", (self.id,))
            conn.commit()
