import requests
import base64
from Crypto.Cipher import AES
from Crypto import Random
import json

BS = 32
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class _AESCipher:

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

class PyTwoFaas():

  url = "http://127.0.0.1:5000"

  def __init__(self, companyToken, publicKey):
    self.cToken = companyToken
    self.publicKey = publicKey

  def _encryptData(self, payload):
    cipher = _AESCipher(self.cToken)
    v =  cipher.encrypt(json.dumps(payload))
    data = { 'publicKey': self.publicKey, 'data' : v }
    print data
    return data

  def sendAuth(self, clientId, factor, authType):
    if authType is not "email":
      payload = { 'userID' : clientId, 'compTK': self.cToken, 'userNum': factor }
    else:
      payload = { 'userID' : clientId, 'compTK': self.cToken, 'userEmail': factor }
  
    data = self._encryptData(payload)

    r = requests.post(self.url + "/init/" + authType, data=data)
    return r.json()

  def sendAuthSMS(self, clientId, phoneNum):
    self.sendAuth(clientId, phoneNum, "sms")

  def sendAuthCall(self, clientId, phoneNum):
    self.sendAuth(clientId, phoneNum, "call")

  def sendAuthEmail(self, clientId, email):
    self.sendAuth(clientId, email, "email")

  def sendUserInput(self, clientId, code):
    payload = {'userID' :clientId,'compTK':self.cToken,'twoAuth':code}
    data = self._encryptData(payload)
    r = requests.post(self.url + "/validate", data=data)
    return r.json()

  def isAuthenticatedUser(self, clientId):
    payload = { 'userID': clientId, 'compTK':self.cToken}
    data = self._encryptData(payload)
    r = requests.post(self.url + "/valid", data=data)
    return r.json()