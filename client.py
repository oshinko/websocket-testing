import socket
import sys

import utils

host, port = sys.argv[1], int(sys.argv[2])
user_agent = 'MySocketClient/0.0'.encode()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    nonce = utils.new_nonce()
    s.sendall(b'GET / HTTP/1.1\r\n')
    s.sendall(f'Host: {host}:{port}\r\n'.encode())
    s.sendall(b'Upgrade: WebSocket\r\n')
    s.sendall(b'Connection: Upgrade\r\n')
    s.sendall(b'Sec-WebSocket-Version: 13\r\n')
    s.sendall(b'Sec-WebSocket-Key: ' + nonce + b'\r\n')
    s.sendall(b'Accept: */*\r\n')
    s.sendall(b'Accept-Encoding: gzip, deflate\r\n')
    s.sendall(b'User-Agent: ' + user_agent + b'\r\n')
    s.sendall(b'\r\n')
    headers = utils.read_headers(s)
    print(headers)
    accept_hash = utils.new_accept_hash(nonce).decode()
    assert accept_hash == headers['sec-websocket-accept']
    print(s.recv(1024))
