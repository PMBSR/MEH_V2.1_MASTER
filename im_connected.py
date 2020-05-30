import socket

def im_connected():
    try:
        socket.create_connection(('Google.com',80))
        return 1
    except OSError:
        return 0
