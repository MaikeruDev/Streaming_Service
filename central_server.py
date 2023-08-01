import socket
import threading

class CentralServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.streams = {}

    def handle_client(self, client_socket):
        print(f'Starting stream to {client_socket.getpeername()}')
        while True:
            try: 
                message = client_socket.recv(1024).decode() 
                message_parts = message.split(' ')
                command = message_parts[0]

                if command == 'register':
                    stream_id, ip, port = message_parts[1], message_parts[2], int(message_parts[3]) 
                    self.streams[stream_id] = (ip, port)
                    print(f'Sending active streams to client: {stream_id} {ip}:{port}')
                    client_socket.send('OK'.encode())
                elif command == 'alive':
                    stream_id, ip, port = message_parts[1], message_parts[2], int(message_parts[3]) 
                    self.streams[stream_id] = (ip, port)
                    print(f'Alive stream: {stream_id} {ip}:{port}')
                    client_socket.send('OK'.encode())
                elif command == 'request':
                    active_streams = '\n'.join(f'{stream_id} {ip}:{port}' for stream_id, (ip, port) in self.streams.items())
                    client_socket.send(active_streams.encode())
            except Exception as e:
                print(f'Error in handle_client: {e}')
                break
        print(f'Ended stream to {client_socket.getpeername()}')
 
    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f'Accepted connection from {addr}')
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
 
if __name__ == "__main__":
    central_server = CentralServer('localhost', 9999)
    central_server.run()
