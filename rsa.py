import hashlib
from os import urandom

from miller_rabin import get_prime_n_bits

def mask(data, seed, mlen):
    t = b''
    for counter in range(ceil(mlen / 20)):
        c = counter.to_bytes(4, "big")
        t += hashlib.sha3_256(seed + c).digest()
    return bytes(map(xor, data, bytes(len(data)) + t[:mlen]))

def gen_keys():
    p = get_prime_n_bits(1024)
    q = get_prime_n_bits(1024)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi_n)
    public_key = (n, e)
    private_key = (n, d)
    return (public_key, private_key)

def oaep_encode(n, message):
    k = (n.bit_length() + 7) // 8
    message_len = len(str(message))
    hash_len = 20
    lable_hash = b"\xda9\xa3\xee^kK\r2U\xbf\xef\x95`\x18\x90\xaf\xd8\x07\t"
    padding_string = b"\x00" * (k - message_len - 2 * hash_len - 2)
    data_block = lable_hash + padding_string + b'\x01' + b'{message}'
    seed = urandom(hash_len)
    masked_data_block = mask(data_block, seed, k - hash_len - 1)
    masked_seed = mask(seed, masked_data_block, hash_len)
    return b'\x00' + masked_seed + masked_data_block

def oaep_decode(n, em):
    k = (n.bit_length() + 7) // 8
    hash_len = 20
    _, masked_seed, masked_data_block = em[:1], em[1:1 + hash_len], em[1 + hash_len:]

    seed = mask(masked_seed, masked_data_block, hash_len)
    data_block = mask(masked_data_block, seed, k - hash_len - 1)
    _, message = data_block.split(b'\x01')
    return message

def rsa(key, message):
    n, exponent = key
    k = (n.bit_length() + 7) // 8
    m = int.from_bytes(message, "big")
    c = pow(m, exponent, n)
    return c.to_bytes(k, "big")

def verify_signature(public_key, signature):
    with open('example.txt', 'rb') as file:
        newcontent = file.read()

        rsa_signature = rsa(public_key, signature)[-32:]
        
        return rsa_signature == hashlib.sha3_256(newcontent).digest()
