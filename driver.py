from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route('/') 
def index():
    return 'Index!'

#this initializes the 2 factor process once company validates 1st auth 
@app.route('/init', methods=['POST'])
def template():
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    return ("clientID: client  <br> phoneNumber: 123-456-7890 <br> companyToken: dshnvu9498hjs")
    

@app.route('/admin')
def admin():
    return 'Admin'

@app.route('/firstlogInDone')
def auth():
    #gets phone number, and the auth token set my sys admin and sends code to user. 
    #write the user code, phone number, and user id to db 
    return 'Authorize'

@app.route('/validate')
def val():
    #gets the user id, phone number, and code and compares that to db
    return 'Validate'

@app.route('/login')
def log_in():
    return app.send_static_file('login.html')

@app.route('/two_factor')
def two_factor():
    return app.send_static_file('twofac.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
