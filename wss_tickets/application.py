from flask import Flask
from equitys import all_equitys
from flask import jsonify

application = Flask(__name__)

@application.route("/tickets")
def all():
    ativos = all_equitys()    
    return jsonify(ativos)
