from flask import Flask,jsonify
from equitys import all_equitys


application = Flask(__name__)

@application.route("/")
def all():
    application.logger.info("serviço solicitado")
    ativos = all_equitys()    
    return jsonify(ativos)

