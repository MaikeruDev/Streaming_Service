import socket
import struct
import cv2
import numpy as np
import pickle

central_server_ip = 'localhost'
central_server_port = 9999

def get_streams(): 
    try:
        central_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        central_server_socket.connect((central_server_ip, central_server_port))
        central_server_socket.send('request'.encode()) 
        
        data = b""
        while True:
            part = central_server_socket.recv(1024)
            data += part
            if len(part) < 1024: 
                break
        
        streams = data.decode() 

        central_server_socket.close() 
        return [stream.split(' ') for stream in streams.split('\n') if stream]

    except Exception as e:
        print(f'Error in get_streams: {e}')
        return []

def receive_stream(stream_ip, stream_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((stream_ip, stream_port))
        print(f'Connected to {stream_ip}:{stream_port}')
        client_socket.send('ready'.encode())

        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data) 
            frame = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.namedWindow("RECEIVING VIDEO", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("RECEIVING VIDEO", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("RECEIVING VIDEO", frame) 
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    except Exception as e:
        print(f'Error occurred in receive_stream: {e}')
    finally:
        client_socket.close()
        """ cv2.destroyAllWindows() """
        input("e")

def main():
    streams = get_streams() 
    if not streams:
        print("No active streams available.")
        return

    for i, (stream_id, stream_ip_port) in enumerate(streams):
        print(f'{i+1}. {stream_id} {stream_ip_port}')

    selected_stream = int(input("Select a stream: ")) - 1
    if selected_stream < 0 or selected_stream >= len(streams):
        print("Invalid selection.")
        return

    stream_id, stream_ip_port = streams[selected_stream]
    stream_ip, stream_port = stream_ip_port.split(':')
    print(f'You selected: {stream_id} {stream_ip_port}. Connecting...')
    receive_stream(stream_ip, int(stream_port))

if __name__ == "__main__":
    main()
