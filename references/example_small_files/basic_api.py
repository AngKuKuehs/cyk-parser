from flask import Flask
from flask import request

import ast
import json

app = Flask(__name__)
@app.route("/", methods=["GET"])
def default_route():
    """
    Returns a string
    """
    return "Landing page for to-do-list project"

@app.route("/req", methods=["POST"])
def req():
    myreq = request.data
    my_req = myreq.decode()
    my_req = eval(my_req)
    return my_req

if __name__ == "__main__":
    app.run(debug=True)
