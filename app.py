from flask import Flask, render_template, redirect, request
from recipe_model import Ingredient, Recipe


app = Flask(__name__)
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
        # TODO: Flash an error
        return redirect("/recipes")


if __name__ == "__main__":
    app.run(debug=True)
