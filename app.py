from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/recipes")


@app.route("/recipes")
def recipes():
    return render_template("index.html", recipes=Recipe.all())
