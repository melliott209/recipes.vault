from flask import Flask, render_template, redirect, request
from recipe_model import Recipe


app = Flask(__name__)


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
    r = Recipe(request.form["title"], request.form["desc"], [], [])
    r.save()  # TODO: check if this errors or not
    return redirect("/recipes")


@app.route("/recipes/new/new-ingredient", methods=["GET"])
def new_ingredient():
    return render_template("new_ingredient.html")


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
