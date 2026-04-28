from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import Recipe

# Define the blueprint for recipe routes
recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/recipes')
def list_recipes():
    """
    顯示所有食譜列表頁面。
    邏輯：呼叫 Recipe.get_all() 並渲染 index.html。
    """
    recipes = Recipe.get_all()
    return render_template('recipes/index.html', recipes=recipes)

@recipe_bp.route('/recipes/new', methods=['GET'])
def new_recipe_form():
    """
    顯示新增食譜的表單頁面。
    邏輯：渲染 new.html。
    """
    return render_template('recipes/new.html')

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    處理新增食譜的表單送出。
    邏輯：接收 POST 資料，建立 Recipe，成功後重導向至列表。
    """
    title = request.form.get('title')
    description = request.form.get('description')
    cooking_time = request.form.get('cooking_time_minutes')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')

    # 基本驗證
    if not title:
        flash('食譜名稱為必填欄位！', 'danger')
        return render_template('recipes/new.html')

    data = {
        'title': title,
        'description': description,
        'cooking_time_minutes': cooking_time,
        'ingredients': ingredients,
        'steps': steps
    }

    recipe_id = Recipe.create(data)
    if recipe_id:
        flash('食譜新增成功！', 'success')
        return redirect(url_for('recipe.list_recipes'))
    else:
        flash('新增失敗，請稍後再試。', 'danger')
        return render_template('recipes/new.html')

@recipe_bp.route('/recipes/<int:id>')
def recipe_detail(id):
    """
    顯示單筆食譜的詳細資訊頁面。
    邏輯：呼叫 Recipe.get_by_id(id)，若無則回傳 404。
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜。', 'warning')
        return redirect(url_for('recipe.list_recipes'))
    return render_template('recipes/detail.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe_form(id):
    """
    顯示編輯食譜的表單頁面。
    邏輯：取得現有資料並渲染 edit.html。
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜。', 'warning')
        return redirect(url_for('recipe.list_recipes'))
    return render_template('recipes/edit.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    處理更新食譜的表單送出。
    邏輯：接收 POST 資料，更新 DB，成功後重導向至詳細頁。
    """
    title = request.form.get('title')
    description = request.form.get('description')
    cooking_time = request.form.get('cooking_time_minutes')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')

    if not title:
        flash('食譜名稱為必填欄位！', 'danger')
        recipe = Recipe.get_by_id(id)
        return render_template('recipes/edit.html', recipe=recipe)

    data = {
        'title': title,
        'description': description,
        'cooking_time_minutes': cooking_time,
        'ingredients': ingredients,
        'steps': steps
    }

    if Recipe.update(id, data):
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipe.recipe_detail', id=id))
    else:
        flash('更新失敗，請稍後再試。', 'danger')
        recipe = Recipe.get_by_id(id)
        return render_template('recipes/edit.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    處理刪除食譜的請求。
    邏輯：執行刪除並重導向至列表。
    """
    if Recipe.delete(id):
        flash('食譜已刪除。', 'success')
    else:
        flash('刪除失敗，請稍後再試。', 'danger')
    return redirect(url_for('recipe.list_recipes'))
