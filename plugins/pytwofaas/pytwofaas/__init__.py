import requests

class PyTwoFaas():

  url = "http://127.0.0.1:5000"

  def __init__(self, companyToken):
    self.cToken = companyToken
    print self.cToken

  def sendAuth(self, clientId, phoneNum):
    payload = { 'userID' : clientId, 'compTK': self.cToken, 'userNum': phoneNum }
    r = requests.post(self.url + "/init", data=payload)
    print(r.text)

  def sendUserInput(self, clientId, code):
    payload = {'userID' :clientId,'compTK':self.cToken,'twoAuth':code}
    r = requests.post(self.url + "/validate", data=payload)
    print(r.text)