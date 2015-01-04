from flask import Flask, request, jsonify
from flask import render_template
from pytwofaas import PyTwoFaas
import json

app = Flask(__name__)

@app.route('/') 
def index():
    return render_template('layout.html')

@app.route('/login', methods=['POST']) 
def login():
    print "WOOOOO"
    error = None

    #############
    #
    #
    # Company will have authentication here
    #
    #
    ##############
    username = request.form['username']
    phone = "+972527482538"



    print "WOOWOOOW"

    ###################### PYTWOFAAS

    myTwoFass = PyTwoFaas("6D6997D5-AC88-4747-847B-C5BB3AB0", "4C351914-71D7-4A7A-B41E-E8C33070")
    v = myTwoFass.sendAuthSMS(username, phone)

    #####################

    if v['success'] == 'true':
        return render_template('second_factor.html', username=username)
    else:
        return render_template('failure.html')

@app.route('/validate', methods=['POST']) 
def validate():
    error = None
    username = request.form['username']
    secondFact = request.form['2fact']

    p = PyTwoFaas("6D6997D5-AC88-4747-847B-C5BB3AB0", "4C351914-71D7-4A7A-B41E-E8C33070")
    v = p.sendUserInput(username, secondFact)

    if v['success'] == 'true':
        return render_template('success.html')
    else:
        return render_template('failure.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=3000)