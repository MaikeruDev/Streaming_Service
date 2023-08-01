import socket
import threading
import time
import pyautogui 
import numpy as np
from PIL import ImageGrab
import socket, cv2, pickle, struct, imutils

central_server_ip = 'localhost'  # Central server IP
central_server_port = 9999  # Central server port
 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name) # Own server IP
port = 12345 # Own server port
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)

central_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
central_server_socket.connect((central_server_ip, central_server_port))
message = f'register stream1 {host_ip} {port}'.encode()
bytes_sent = central_server_socket.send(message) 
central_server_socket.recv(1024)

def send_alive_messages():
    while True:
        message = f'alive stream1 {host_ip} {port}'.encode()
        bytes_sent = central_server_socket.send(message) 
        central_server_socket.recv(1024)
        time.sleep(5)

def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        if message == 'ready':
            print("Client is ready. Starting to send stream.")
            
            try:
                while True: 
                    img = pyautogui.screenshot() 
                    frame = np.array(img) 
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                    result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100]) 
                    a = pickle.dumps(frame, 0)
                    message = struct.pack("Q", len(a)) + a

                    client_socket.sendall(message) 

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    
                cv2.destroyAllWindows()

            except Exception as e:
                print(f"Error occurred during stream: {e}")
                break
        else:
            print(f"Unknown command: {message}")
            break


def main():
    threading.Thread(target=send_alive_messages).start()

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Accepted connection from {addr}')
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    main()
