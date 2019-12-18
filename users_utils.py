import hashlib
import json
#Path fixer
import sys
sys.path.insert(0, '/var/www/front_end_walker')
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