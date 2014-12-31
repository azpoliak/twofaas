import requests

class PyTwoFaas():

  url = "http://127.0.0.1:5000"

  def __init__(self, companyToken):
    self.cToken = companyToken
    print self.cToken

  def sendAuth(self, clientId, factor, authType):
    if authType is not "email":
      payload = { 'userID' : clientId, 'compTK': self.cToken, 'userNum': factor }
    else:
      payload = { 'userID' : clientId, 'compTK': self.cToken, 'userEmail': factor }
    r = requests.post(self.url + "/init/" + authType, data=payload)
    return r.json()

  def sendAuthSMS(self, clientId, phoneNum):
    self.sendAuth(clientId, phoneNum, "sms")

  def sendAuthCall(self, clientId, phoneNum):
    self.sendAuth(clientId, phoneNum, "call")

  def sendAuthEmail(self, clientId, email):
    self.sendAuth(clientId, email, "email")

  def sendUserInput(self, clientId, code):
    payload = {'userID' :clientId,'compTK':self.cToken,'twoAuth':code}
    r = requests.post(self.url + "/validate", data=payload)
    return r.json()

  def isAuthenticatedUser(self, clientId):
    payload = { 'userID': clientId, 'compTK':self.cToken}
    r = requests.post(self.url + "/valid", data=payload)
    return r.json()