import requests

class PyTwoFaas(companyToken):

	url = "http://127.0.0.1:5000"

	def init(clientId, phoneNum):
    	payload = { 'userID' : clientId, 'compTK': companyToken, 'userNum': phoneNum }
    	r = requests.post(url + "/init", data=payload)
    	print(r.text)

	def validate(clientId, code):
		payload = { 'userID' : clientId, 'compTK': companyToken, 'twoAuth': code }
		r = requests.post(url + "/validate", data=payload)
    	print(r.text)