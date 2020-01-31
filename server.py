import socket
import sys

import utils

host, port = sys.argv[1], int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        headers = utils.read_headers(conn)
        assert headers.get('upgrade', '').lower() == 'websocket'
        assert headers.get('connection', '').lower() == 'upgrade'
        assert headers.get('sec-websocket-version') == '13'
        assert 'sec-websocket-key' in headers
        accept_hash = utils.new_accept_hash(headers['sec-websocket-key'])
        conn.sendall(b'HTTP/1.1 101 Switching Protocols\r\n')
        conn.sendall(b'Upgrade: WebSocket\r\n')
        conn.sendall(b'Connection: Upgrade\r\n')
        conn.sendall(b'Sec-WebSocket-Accept: ' + accept_hash + b'\r\n')
        conn.sendall(b'\r\n')
        conn.sendall(utils.new_frame('Hello!'))
