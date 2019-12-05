import socket
TCP_IP = "45.79.37.223"
TCP_PORT = 25000
BUFFER_SIZE = 1024 * 100

#Primeros 5 digitos: Largo del mensaje incluyendo sinit o getsv o el nombre del servicio

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = socket.gethostbyname(TCP_IP)
s.connect((r, TCP_PORT))
message = "<tx id='borja'><req>auten</req><usr>walker</usr><psw>walker</psw></tx>"
s.send(bytes(str(len(message)).zfill(5) + message, 'utf-8'))
data = s.recv(BUFFER_SIZE)
print(data)