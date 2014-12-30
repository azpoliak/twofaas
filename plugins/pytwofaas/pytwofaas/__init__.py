import requests

class PyTwoFaas():

  url = "http://127.0.0.1:5000"

  def __init__(self, companyToken):
    self.cToken = companyToken
    print self.cToken

  def sendAuthSMS(self, clientId, phoneNum):
    payload = { 'userID' : clientId, 'compTK': self.cToken, 'userNum': phoneNum }
    r = requests.post(self.url + "/init/sms", data=payload)
    print(r.text)

def sendAuthCall(self, cliendId, phoneNum):
    payload = { 'userID' : clientId, 'compTK': self.cToken, 'userNum': phoneNum }
    r = requests.post(self.url + "/init/call", data=payload)
    print(r.text)


  def sendAuthEmail(self, cliendId, email):
    payload = { 'userID' : clientId, 'compTK': self.cToken, 'userEmail': email }
    r = requests.post(self.url + "/init/email", data=payload)
    print(r.text)


  def sendUserInput(self, clientId, code):
    payload = {'userID' :clientId,'compTK':self.cToken,'twoAuth':code}
    r = requests.post(self.url + "/validate", data=payload)
    print(r.text)
