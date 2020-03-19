# -*- coding: utf-8 -*-

from flask import (
    Flask,
    jsonify,
    request
)
import retriever
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Create a URL route in our application for "/"
@app.route('/info')
def info():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    x = retriever.Retriever('/opt/oca/oca-12')
    resp = jsonify(x.getInfo())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, OPTIONS, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Methods, Access-Control-Allow-Origin, Origin, Accept, Content-Type'
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Accept'] = 'application/json'
    return resp

# Create a URL route in our application for "/"
@app.route('/nodes')
def nodes():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    x = retriever.Retriever('/opt/oca/oca-12')
    resp = jsonify(x.getNodes())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, OPTIONS, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Methods, Access-Control-Allow-Origin, Origin, Accept, Content-Type'
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Accept'] = 'application/json'
    return resp

# Create a URL route in our application for "/"
@app.route('/links')
def links():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    x = retriever.Retriever('/opt/oca/oca-12')
    resp = jsonify(x.getLinks())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, OPTIONS, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Methods, Access-Control-Allow-Origin, Origin, Accept, Content-Type'
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Accept'] = 'application/json'
    return resp

# Create a URL route in our application for "/"
@app.route('/moduleNet', methods=['POST'])
def moduleNet():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    x = retriever.Retriever('/opt/oca/oca-12')

    if not request.form:
        return False
    resp = jsonify(x.getNetModule([i for i in request.form][0]))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, OPTIONS, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Methods, Access-Control-Allow-Origin, Origin, Accept, Content-Type'
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Accept'] = 'application/json'
    return resp

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)