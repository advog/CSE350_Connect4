import random
import socket
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

rcv = ""

def connect_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((HOST, PORT))
        sock.settimeout(60*5)
        return 0, sock
    except socket.error:
        sock.close()
        return -1, 0

#accepts (string, function) [] of (msg_key, routine)
#returns -1 for socket read error, else whatever the first return for the routine is
def look_for(sock, routines):
    global rcv
    while True:
        try:
            data = sock.recv(128)
        except socket.error:
            return -1
        rcv = rcv + data.decode(encoding="ascii")

        completed = []
        brackets = 0
        offset = 0

        for i in range(len(rcv)):
            if rcv[i] == '{':
                brackets += 1
            elif rcv[i] == '}':
                brackets -= 1
                if brackets == 0:
                    completed.append(json.loads(rcv[offset: i+1]))
                    offset = i+1
        rcv = rcv[offset:]

        for j in completed:
            for r in routines:
                if j["msg"] == r[0]:
                    return r[1](j)

#sends request for code to server, returns -1 for error, returned code otherwise
def request_code_ret(j):
    return j["code"]
def request_code(sock):
    send_me = json.dumps({"msg":"request_code"})
    try:
        sock.sendall(bytes(send_me, encoding = "ascii"))
    except socket.error:
        return -1

    routines = [("request_code", request_code_ret)]
    return look_for(sock, routines)

#sends code to server, returns -1 for socket error, 0 otherwise
def send_code(sock, code):
    send_me = json.dumps({"msg": "send_code" , "code": code})
    try:
        sock.sendall(bytes(send_me, encoding = "ascii"))
        return 0
    except socket.error:
        return -1

#helper function
def disconnect_ret(j):
    return -1

#waits until server sends start game msg, returns -1 if timeout, 0 if succesful
def wait_start_ret(j):
    return 0
def wait_start(sock):
    routines = [("start", wait_start_ret)]
    return look_for(sock, routines)

#waits for move to be sent by server, returns -1 if timeout, column otherwise
def request_mov_ret(j):
    return j["column"]
def request_move(sock):
    routines = [("start", wait_start_ret), ("disconnect", disconnect_ret)]
    return look_for(sock, routines)


#sends move to server, returns -1 if socket error, 0 if otherwise
def send_move(sock, column):
    send_me = json.dumps({"msg": "move", "column": column})
    try:
        sock.sendall(bytes(send_me, encoding = "ascii"))
        return 0
    except socket.error:
        return -1

def echo_raw(sock):
    while True:
        try:
            data = sock.recv(128)
            print(data.decode(encoding = 'ascii'))
        except socket.error:
            return -1


#status, sock = connect_server()

#send_move(sock, 1)
#echo_raw(sock)



