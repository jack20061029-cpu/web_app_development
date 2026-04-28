from flask import Blueprint, render_template, request, redirect, url_for

# Define the blueprint for recipe routes
recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/recipes')
def list_recipes():
    """
    顯示所有食譜列表頁面。
    邏輯：呼叫 Recipe.get_all() 並渲染 index.html。
    """
    pass

@recipe_bp.route('/recipes/new', methods=['GET'])
def new_recipe_form():
    """
    顯示新增食譜的表單頁面。
    邏輯：渲染 new.html。
    """
    pass

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    處理新增食譜的表單送出。
    邏輯：接收 POST 資料，建立 Recipe，成功後重導向至列表。
    """
    pass

@recipe_bp.route('/recipes/<int:id>')
def recipe_detail(id):
    """
    顯示單筆食譜的詳細資訊頁面。
    邏輯：呼叫 Recipe.get_by_id(id)，若無則回傳 404。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe_form(id):
    """
    顯示編輯食譜的表單頁面。
    邏輯：取得現有資料並渲染 edit.html。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    處理更新食譜的表單送出。
    邏輯：接收 POST 資料，更新 DB，成功後重導向至詳細頁。
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    處理刪除食譜的請求。
    邏輯：執行刪除並重導向至列表。
    """
    pass
