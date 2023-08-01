# Live Streaming System

A multi-server live streaming system that allows multiple servers to stream their screens to clients through a central server.

## System Architecture

The system is composed of three components:

1. **Stream Servers**: They stream their screens to clients. They register and keep alive connections with the central server.
2. **Central Server**: It keeps track of active stream servers. Clients can request the list of active servers from the central server.
3. **Clients**: They get the list of active servers from the central server, and can connect to stream servers to view their screens.

## Setup

The system is implemented in Python. To run it, you need Python 3.7 or later. 

### Install Dependencies

Install the required dependencies using the following command:

    pip install -r requirements.txt


### Run the Servers

1. To start the central server, run:

    ```
    python central_server.py
    ```
    
2. To start a stream server, run:

    ```
    python stream_server.py
    ```

### Run the Client

To start a client, run:

    python client.py
 

## Contribution

Feel free to contribute to this project by creating a pull request.
 
