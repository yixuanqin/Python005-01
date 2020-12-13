import socket

HOST = socket.gethostname()
PORT = 9899
SIZE = 1024

def file_sender_server(): 
    '''
        sender server: send file to client
    '''    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print("Server is listening ...")
    while True:
        conn, addr = s.accept()
        print("Get connection from", addr)
        data = conn.recv(SIZE)
        print("Receive from client:", data)
        if data.decode() == "Ready":
            with open("server_send.txt", 'rb') as f:
                content = f.read(SIZE)
                while content:
                    conn.sendall(content)
                    content = f.read(SIZE)
            print("File has sent to", addr)
            conn.close()
    s.close()

def file_receiver_server():
    '''
        receiver server: receive file from client
    '''      
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print("Server is listening ...")
    while True:
        conn, addr = s.accept()
        print("Get connection from", addr)
        data = conn.recv(SIZE)
        file_name = data.decode()
        with open(file_name, 'wb') as f:
            content = conn.recv(SIZE)
            while content:
                f.write(content)
                content = conn.recv(SIZE)
        print("Get the file successfully:", file_name)
        conn.close()
    s.close()

if __name__ == '__main__':
    # file_sender_server()
    file_receiver_server()
