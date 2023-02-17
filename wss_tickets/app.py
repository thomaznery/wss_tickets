from flask import Flask
from equitys import all_equitys
import json
from flask import jsonify

app = Flask(__name__)

@app.route("/tickets")
def all():
    ativos = all_equitys()
    
    return jsonify(ativos)

if __name__ == "__main__":
   app.run()