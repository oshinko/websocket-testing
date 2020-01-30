def new_packet(payload, masking_key=None):
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
    r = bytearray(int.to_bytes(bits, n_bytes, 'big'))
    r.extend(payload_bin)
    return r
