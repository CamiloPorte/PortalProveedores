import socket
BUFFER_SIZE = 1024

def get_response_length(message):
	return int(message[:5])

def cut_response_length(message):
	return message[5:]

def connect(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r = socket.gethostbyname(ip)
    s.connect((r, port))
    return s

def send(s, message):
    strlen = str(len(message)).zfill(5)
    s.send(bytes(strlen + str(message), 'utf-8'))

def receive(s):
	result = b""
	received = s.recv(BUFFER_SIZE)
	result += received
	rec_len = get_response_length(received)
	#print("rec_len: ", rec_len)
	#print("received: ", received)
	response_length = len(received)
	rec_len -= response_length
	while rec_len > 0:
		received = s.recv(BUFFER_SIZE)
		result += received
		response_length = len(received)
		rec_len -= response_length
		#print("rec_len: ", rec_len)
		#print("received: ", received)
	return cut_response_length(result)