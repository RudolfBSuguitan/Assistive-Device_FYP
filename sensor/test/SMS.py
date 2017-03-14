#uses python 3

import urllib.request
import urllib.parse
import json

username='rudolf.suguitan@gmail.com'
hash='8ccd3db77b599470043a86b64d1bafbe806e254294c2d538ff8fba887064f8e2'
sender='RudolfS'
receiver='353861608499'
message='Please check your email. A user needs assistance'
 
def sendSMS(uname, hashCode, numbers, sender, message):
	try:
		data =  urllib.parse.urlencode({'username': uname, 'hash': hashCode, 'numbers': numbers, 'message' : message, 'sender': sender})
		data = data.encode('utf-8')
		request = urllib.request.Request("http://api.txtlocal.com/send/?")
		f = urllib.request.urlopen(request, data)
		fr = f.read().decode('utf-8')
		return fr
	except:
		error="Errorrrr"
		return error 
resp =  sendSMS(username, hash, receiver, sender, message)
print (resp)
msg=json.loads(resp)
print (msg['status'])
