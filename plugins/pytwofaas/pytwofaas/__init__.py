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
    print(r.text)

  def sendAuthSMS(self, clientId, phoneNum):
    self.sendAuth(clientId, phoneNum, "sms")

  def sendAuthCall(self, clientId, phoneNum):
    self.sendAuth(clientId, phoneNum, "call")

  def sendAuthEmail(self, clientId, email):
    self.sendAuth(clientId, phoneNum, "email")

  def sendUserInput(self, clientId, code):
    payload = {'userID' :clientId,'compTK':self.cToken,'twoAuth':code}
    r = requests.post(self.url + "/validate", data=payload)
    print(r.text)

  def isAuthenticatedUser(self, clientId):
    payload = { 'userID': clientId, 'compTK':self.cToken}
    r = requests.post(self.url + "/valid", data=payload)
    print(r.text)

p = PyTwoFaas("6D6997D5-AC88-4747-847B-C5BB3AB047A9")
print p.isAuthenticatedUser('gil.chenzion@aqw.com')
#+19736504192
#+972527482538