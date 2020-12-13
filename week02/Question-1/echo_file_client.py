import socket
import os

HOST = socket.gethostname()
PORT = 9899
SIZE = 1024
def file_receiver_client():  
    '''
        receiver client: receive file from server
    '''  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    with open("client_receive.txt", 'wb') as f:
        print("Start to receive file")
        data = "Ready"
        s.sendall(data.encode())
        content = s.recv(SIZE))
        while content:
            f.write(content)
            content = s.recv(SIZE))
    print('Get the file successfully')
    s.close()
    print('Connection closed')

def file_sender_client(file_path):
    '''
        sender client: send file to server
    '''  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    with open(file_path, 'rb') as f:
        file_name = os.path.basename(f.name)
        print("Start to send file:", file_name)
        s.sendall(file_name.encode())
        content = f.read(SIZE))
        while content:
            s.sendall(content)
            content = f.read(SIZE))
    print('Send file successfully:', file_name)
    s.close()
    print('Connection closed')

if __name__ == '__main__':
    # file_receiver_client()
    file_path = "./files/client_send.txt"
    file_sender_client(file_path)
