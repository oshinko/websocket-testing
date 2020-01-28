import base64
import hashlib
import socket

HOST = ''
PORT = 8000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        data = bytearray()
        while not data.endswith(b'\r\n\r\n'):
            data.extend(conn.recv(1024))
        _, *header = data.decode().strip().splitlines()
        headers = {}
        for line in header:
            name, value = line.split(': ', 1)
            headers[name.lower()] = value
        assert headers.get('upgrade', '').lower() == 'websocket'
        assert headers.get('connection', '').lower() == 'upgrade'
        assert headers.get('sec-websocket-version') == '13'
        assert 'sec-websocket-key' in headers
        nonce = headers['sec-websocket-key']
        uuid = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        encoded = (nonce + uuid).encode()
        accept_hash = base64.b64encode(hashlib.sha1(encoded).digest())
        conn.sendall(b'HTTP/1.1 101 Switching Protocols\r\n')
        conn.sendall(b'Upgrade: WebSocket\r\n')
        conn.sendall(b'Connection: Upgrade\r\n')
        conn.sendall(b'Sec-WebSocket-Accept: ' + accept_hash + b'\r\n')
        conn.sendall(b'\r\n')
        payload = 'Hello!'
        fin = 0b1
        rsv = 0b000
        opcode = 0x1
        mask = 0b0
        payload_len = len(payload)
        meta = fin << 3 | rsv
        meta = meta << 4 | opcode
        meta = meta << 1 | mask
        meta = meta << 7 | payload_len
        meta = int.to_bytes(meta, 2, 'big')
        data = meta + payload.encode()
        conn.sendall(data)
