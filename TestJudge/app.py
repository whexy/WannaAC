from flask import Flask, request, jsonify
from flask_cors import CORS
from time import sleep
from random import sample
from random import randint
from testjudge import *
from getwelcomeinfo import *

app = Flask(__name__)
CORS(app)

@app.route('/submit/', methods=['POST'])
def submit():
    code = request.get_json()
    print(code)
    res = judge_impl(code)
    print(res)
    return jsonify(res)

@app.route('/submitdata/', methods=['POST'])
def submitdata():
    data = request.get_json()
    print(data)
    res = save_new_data(data)
    print(res)
    return jsonify(res)

@app.route('/problemset/')
def problemset():
    return jsonify(get_prob_list())

@app.route('/wc/')
def welcome():
    return jsonify(getinfo())

@app.route('/wcinfo/')
def modify():
    newinfo = request.args.get("info")
    setinfo(newinfo)
    return jsonify("Success")

if __name__ == '__main__':
    app.run('0.0.0.0',5000)
