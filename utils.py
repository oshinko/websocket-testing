import base64
import hashlib
import secrets


def read_headers(s):
    data = bytearray()
    while not data.endswith(b'\r\n\r\n'):
        data.extend(s.recv(1))
    headers = {}
    for i, line in enumerate(data.decode().strip().splitlines()):
        if i > 0:
            name, value = line.split(': ', 1)
            headers[name.strip().lower()] = value.strip()
    return headers


def new_nonce():
    return base64.b64encode(secrets.token_bytes(16))


def new_accept_hash(nonce):
    if isinstance(nonce, (bytearray, bytes)):
        nonce = nonce.decode()
    uuid = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    encoded = (nonce + uuid).encode()
    return base64.b64encode(hashlib.sha1(encoded).digest())


def new_frame(payload, masking_key=None):
    bits = 0b100000000
    if isinstance(payload, str):
        bits |= 0b000000010
        payload_bin = payload.encode()
    elif isinstance(payload, (bytearray, bytes)):
        bits |= 0b000000100
        payload_bin = payload
    else:
        raise TypeError
    if masking_key:
        bits |= 0b000000001
    payload_len = len(payload_bin)
    if payload_len <= 125:
        bits = bits << 7 | payload_len
        n_bits = 16
    elif payload_len <= 65535:
        bits = bits << 7 | 0b1111110
        bits = bits << 16 | payload_len
        n_bits = 32
    else:
        bits = bits << 7 | 0b1111111
        bits = bits << 64 | payload_len
        n_bits = 80
    n_bytes = int(n_bits / 8)
    b = bytearray(int.to_bytes(bits, n_bytes, 'big'))
    b.extend(payload_bin)
    return bytes(b)


def parse_frame(raw):
    # payload = 'Hello!'
    # fin = 0b1
    # rsv = 0b000
    # opcode = 0x1
    # mask = 0b0
    # payload_len = len(payload)
    # meta = fin << 3 | rsv
    # meta = meta << 4 | opcode
    # meta = meta << 1 | mask
    # meta = meta << 7 | payload_len
    # meta = int.to_bytes(meta, 2, 'big')
    # data = meta + payload.encode()
    opcode = 0x01
    payload = 'Dummy'
    return opcode, payload
