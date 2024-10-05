from flask import Flask, render_template, redirect, request, flash
from recipe_model import Ingredient, Recipe


app = Flask(__name__)
app.secret_key = b'sm1?7,HBxd0@'
Recipe.load_db()


@app.route("/")
def index():
    return redirect("/recipes")


@app.route("/recipes")
def recipes():
    return render_template("index.html", recipes=Recipe.all())


@app.route("/recipes/new", methods=["GET"])
def new_recipe_get():
    return render_template("new.html")


@app.route("/recipes/new", methods=["POST"])
def new_recipe():
    ingredients_data = request.form.getlist("ingredient")[:-1]
    qty_data = request.form.getlist("qty")[:-1]
    unit_data = request.form.getlist("unit")[:-1]
    ingredients = []
    for idx, i in enumerate(ingredients_data):
        ingredients.append(Ingredient(i, int(qty_data[idx]), unit_data[idx]))
    instructions = request.form.getlist("instruction")[:-1]
    r = Recipe(request.form["title"], request.form["desc"], ingredients, instructions)
    r.save()  # TODO: check if this errors or not
    flash(f"Successfully created recipe: {r.name()}")
    return redirect("/recipes")


@app.route("/recipes/new/new-ingredient", methods=["GET"])
def new_ingredient():
    return render_template("new_ingredient.html")


@app.route("/recipes/new/new-instruction")
def new_instruction():
    return render_template("new_instruction.html")


@app.route("/recipes/<int:id>")
def recipe_get(id):
    recipe = Recipe.get_by_id(id)
    if recipe is not None:
        return render_template("recipe.html", recipe=recipe)
    else:
        flash("Failed to retrieve recipe!", "error")
        return redirect("/recipes")


@app.route("/recipes/<int:id>/edit")
def recipe_edit_get(id):
    recipe = Recipe.get_by_id(id)
    if recipe is None:
        recipe = Recipe("", "", [], [])
    return render_template("edit.html", recipe=recipe)


@app.route("/recipes/<int:id>", methods=["DELETE"])
def recipe_delete(id):
    if Recipe.delete(id):
        flash("Successfully deleted recipe")
        return redirect("/recipes", 303)
    else:
        flash("Failed to delete recipe!", "error")
        return redirect("/recipes")


@app.route("/recipes/<int:id>", methods=["PUT"])
def recipe_update(id):
    name = request.form["title"]
    desc = request.form["desc"]
    ingredients_data = request.form.getlist("ingredient")[:-1]
    qty_data = request.form.getlist("qty")[:-1]
    unit_data = request.form.getlist("unit")[:-1]
    ingredients = []
    for idx, i in enumerate(ingredients_data):
        ingredients.append(Ingredient(i, int(qty_data[idx]), unit_data[idx]))
    instructions = request.form.getlist("instruction")[:-1]

    recipe = Recipe.get_by_id(id)
    if recipe is not None:
        recipe.update(name, desc, ingredients, instructions)
        flash(f'Successfully updated recipe: {name}')
        return redirect("/recipes", 303)
    else:
        flash("Failed to update recipe!", "error")
    return redirect("/recipes")


if __name__ == "__main__":
    app.run(debug=True)
