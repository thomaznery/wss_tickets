from flask import Flask,jsonify
from wss_tickets.equitys import all_equitys


application = Flask(__name__)

@application.route("/")
def all():
    application.logger.info("serviço solicitado")
    ativos = all_equitys()    
    return jsonify(ativos)

if __name__ == "__main__":
    application.run()