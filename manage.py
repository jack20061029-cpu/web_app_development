import os
import sqlite3
from flask import Flask
from app.routes.recipe_routes import recipe_bp

def create_app():
    app = Flask(__name__, template_folder='app/templates', instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register Blueprints
    app.register_blueprint(recipe_bp)

    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('recipe.list_recipes'))

    return app

def init_db():
    """初始化資料庫並建立資料表"""
    app = create_app()
    db_path = app.config['DATABASE']
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    
    print(f"正在初始化資料庫: {db_path}")
    
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
            
    print("資料庫初始化完成！")

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
