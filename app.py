from flask import Flask,render_template
from landsatxplore import __init__ as landsatexplore

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/landsat")
def landsat():
    return render_template("landsat.html")


if __name__=="__main__":
    app.run()