from users_utils import *
import getpass
#Path fixer
import sys
sys.path.insert(0, '/var/www/front_end_walker')

users_data = load_users_data()
next_id = len(users_data)
while True:
	uname = input("Ingrese nombre de usuario: ")
	if uname in users_data:
		print("Este usuario ya existe.")
		continue
	pswd = getpass.getpass('Password:')
	pswd_check = getpass.getpass('Repita su Password:')
	if pswd != pswd_check:
		print("Las contraseñas no coinciden.") 
		continue
	users_data[uname] = {"id": next_id, "password": md5ify(pswd)}
	f = open("users.json", "w")
	f.write(json.dumps(users_data))
	f.close()
	print("Usuario creado correctamente.")
	break