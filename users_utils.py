import hashlib
import json
def md5ify(s):
	return hashlib.md5(s.encode()).hexdigest()
def load_users_data():
	try:
		f = open("users.json", "r")
	except:
		raise Exception("Users file missing!")
	raw_data = f.read()
	f.close()
	return json.loads(raw_data)