from flask import Flask, request
from flask import render_template
from twilio.rest import TwilioRestClient

account_sid = "AC2503925359b3b37abbeaaff6d87621f9"
auth_token = "44363a15bca971ddba81edd23cd56ee9"

app = Flask(__name__)

@app.route('/') 
def index():
    return 'Index!'

#this initializes the 2 factor process once company validates 1st auth 
@app.route('/sms', methods=['POST', 'GET'])
def sms():
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    #parses the json and sends to database and user's phone

    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to="+19736504192", from_="+18622775096", body="twofass")
    return ("clientID: client  <br> phoneNumber: 123-456-7890 <br> companyToken: dshnvu9498hjs")
   
@app.route('/call', methods=['POST', 'GET'])
def call():
    #need to get phone number and Company token and userID
    #phone number, company token will be received as json
    #parses the json and sends to database and user's phone

    client = TwilioRestClient(account_sid, auth_token)
    message = client.calls.create(to="+19736504192", from_="+18622775096", 
    	url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")    

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
