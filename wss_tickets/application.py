from flask import Flask,jsonify, render_template
from equitys import all_equitys


application = Flask(__name__, template_folder="./templates")

@application.route("/tickets")
def all():
    ativos = all_equitys()    
    return jsonify(ativos)

@application.route("/")
def index():
    return render_template("index.html")

    