import socket
import gamelogic

host = socket.gethostname()
port = 42068

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

class Game:
    def __init__(self):
        try:
            self.conn1, self.addr1 = sock.accept()
            self.conn2, self.addr2 = sock.accept()
            print("Successful Connections")
        except:
            print("Failed Connections")
            self.conn1 = None
            self.conn2 = None
            self.addr1 = None
            self.addr2 = None
        self.turn = 0
    def progress(self):
        if(self.turn % 2 == 0):
            data = self.conn1.recv(1024)
            self.conn2.sendall(data)
            if not data:
                return False
            print(str(addr1), data)
        else:
            data = self.conn2.recv(1024)
            self.conn1.sendall(data)
            if not data:
                return False
            print(str(addr2), data)
        turn+=1

turn = 0

game = Game()

while game.progress():
    print('Cycled')

play1.close()
play2.close()
