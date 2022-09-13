import hashlib

from miller_rabin import get_prime_128_bits, random_n_bits_number
from aes import AES

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

if __name__ == '__main__': 
    counter = random_n_bits_number(128)

    key = get_prime_128_bits()
    key = hash_128_bits(key)
    aes = AES(key)

    plaintext = sha3("aes.py")
    plaintext_blocks = split_bits(plaintext, 128)

    result = ""
    for block in plaintext_blocks: 
      encrypted_counter = aes.encrypt(counter)
      result += str(encrypted_counter ^ block)
      counter += 1

    print(result)