from flask import Flask, request, jsonify
from flask import render_template
from pytwofaas import PyTwoFaas

app = Flask(__name__)

@app.route('/') 
def index():
    p = PyTwoFaas("6D6997D5-AC88-4747-847B-C5BB3AB047A9")
    print p.sendAuthEmail('bobob', 'gil.chenzio@gmail.com')
    #000d49
    #+19736504192
    #+972527482538
    return 'Index!'

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=3000)
