from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route('/') 
def index():
    return 'Index!'

@app.route('/login')
def log_in():
    return app.send_static_file('login.html')

@app.route('/two_factor')
def two_factor():
    return app.send_static_file('twofac.html')

if __name__ == '__main__':
    app.run()
