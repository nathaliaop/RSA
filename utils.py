import hashlib
import base64

def read_key_from_file(path):
    with open(path, 'r') as file:
        n = int(file.readline())
        ed = int(file.readline())
    
    return (n, ed)

def write_key_on_file(path, key):
    n, ed = key

    with open(path, 'w') as file:
        file.write(f'{n}\n{ed}\n')

def read_from_file(path, mode='r'):
    with open(path, mode) as file:
        content = file.read()
    
    return content

def write_on_file(path, content, mode='w'):
    with open(path, mode) as file:
        file.write(f'{content}\n')

def encode_to_base64(message):
    return base64.b64encode(message).decode('ascii')

def decode_from_base64(message):
    return base64.b64decode(message)

def hash_128_bits(key):
	return int(hashlib.sha3_256(str(key).encode()).hexdigest(), base=16)

def sha3(filename):
        hash_sha3 = hashlib.sha3_256()
        with open(filename, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                hash_sha3.update(block)
        return int(hash_sha3.hexdigest(), base=16)

def split_bits(value, n):
    mask = (1 << n) - 1
    blocks = []
    while value:
        blocks.append(value & mask)
        value >>= n
    blocks.reverse()
    return blocks

def padding(message):
	remainder = 16 - len(message) % 16

	return message + bytes([remainder] * remainder)

def remove_padding(message):
	return message[:-message[-1]]

def split_128bits(message):
	return [message[i:i+16] for i in range(0, len(message), 16)]
