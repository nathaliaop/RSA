import hashlib

from rsa import gen_keys, rsa, verify_signature, oaep_encode, oaep_decode
from miller_rabin import get_prime_n_bits, random_n_bits_number
from aes import AES
from utils import split_128bits, padding, remove_padding, encode_to_base64, decode_from_base64, read_key_from_file, write_key_on_file, read_from_file, write_on_file, hash_128_bits, split_bits, sha3

import argparse

import sys

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('action', choices=['keygen', 'sign', 'verify', 'crypt', 'decrypt'])

    parser.add_argument('--publickey', default='public.key')
    parser.add_argument('--privatekey', default='private.key')

    parser.add_argument('--signature', default='signature.txt')

    parser.add_argument('--file', '-f')

    args = parser.parse_args()

    if args.action == 'keygen':
        public_key, private_key = gen_keys()

        write_key_on_file(args.publickey, public_key)
        write_key_on_file(args.privatekey, private_key)

        print('Chaves geradas com sucesso.')
    elif args.action == 'sign':
        private_key = read_key_from_file(args.privatekey)

        with open(args.file, 'rb') as file:
            content = file.read()

        signature = rsa(private_key, oaep_encode(private_key[0], hashlib.sha3_256(content).digest()))

        write_on_file(args.signature, encode_to_base64(signature))
    elif args.action == 'verify':        
        public_key = read_key_from_file(args.publickey)

        signature = decode_from_base64(read_from_file(args.signature))

        if verify_signature(public_key, signature):
            print('Assinatura válida')
        else:
            print('Assinatura inválida')
    elif args.action == 'crypt':
        counter = random_n_bits_number(128)

        key = get_prime_n_bits(1024)
        key = hash_128_bits(key)

        # salva o counter e a key em um arquivo
        write_on_file('counter.key', f'{counter}\n{key}\n')

        aes = AES(key)

        plaintext = padding(read_from_file(args.file, 'rb'))
        plaintext_splitted = split_128bits(plaintext)

        result = bytes()
        for block in plaintext_splitted:
            counter_encrypted = aes.encrypt(counter)
            
            block_integer = int.from_bytes(block, 'big')

            result += (block_integer ^ counter_encrypted).to_bytes(128 // 8, 'big')

            counter += 1

        write_on_file('counter_encrypted.txt', encode_to_base64(result))

    elif args.action == 'decrypt':
        with open('counter.key', 'r') as file:
            counter = int(file.readline())
            key = int(file.readline())

        aes = AES(key)

        blocks = split_128bits(decode_from_base64(read_from_file('counter_encrypted.txt')))

        plaintext_decrypted = bytes()

        for block in blocks:
            counter_encrypted = aes.encrypt(counter)

            answer_result = counter_encrypted ^ int.from_bytes(block, 'big')

            plaintext_decrypted += answer_result.to_bytes(128//8, 'big')

            counter += 1

        plaintext_decrypted = remove_padding(plaintext_decrypted)

        with open('output.txt', 'wb') as file:
            file.write(plaintext_decrypted)

if __name__ == '__main__': 
    main()
    # apagar coisas de decrypt no aes
    # usar oaep ao assinar

    
    # aes = AES(key)

    # plaintext = encode_to_base64(read_from_file('example.txt', 'rb'))


    # plaintext_splitted = split_128bits(plaintext)

    
    
    # print(result)

    # plaintext = int.from_bytes(plaintext, 'big')

    # multiplo = num_bytes + (128 - num_bytes % 128)
    ''''
    plaintext_decrypted = bytes()

    counter = ini_counter
    for block in result:
        counter_encrypted = aes.encrypt(counter)

        answer_result = counter_encrypted ^ block

        plaintext_decrypted += answer_result.to_bytes(128//8, 'big')

        counter += 1

    print(plaintext_decrypted)
    print()
    print(plaintext)
    '''
    '''
    

    dividir o plaintext em blocos de 128 bits
    pra cada bloco voce criptografa o counter (incremetado sempre) com aes
    faz XOR do counter criptografado com o bloco do plaintext
    depois concatena esses blocos e essa e a resposta

    descriptografar e sh fazer o inverso
    '''

    
    
    # plaintext = plaintext.to_bytes(multiplo, "big")


    # plaintext = encode_to_base64(plaintext)

    # counter_encrypted = aes.encrypt(plaintext)
    '''
    result = counter_encrypted ^ plaintext

    print(plaintext)

    # decode_from_base64(message)

    plaintext_decrypted = result ^ counter_encrypted

    print(plaintext_decrypted)

    print(plaintext == plaintext_decrypted)

    # print(plaintext)

    # print(plaintext)
    plaintext = int.from_bytes(plaintext, "big")
    plaintext_blocks = split_bits(plaintext, 128)

    result = ""
    for block in plaintext_blocks: 
        encrypted_counter = aes.encrypt(counter)
        result += str(encrypted_counter ^ block)
        counter += 1

    # plaintext = 0b110110110110

    print(plaintext)

    result = aes.encrypt(plaintext)

    result = aes.decrypt(result)

    print(result)

    # result2 = result.to_bytes(128, "big")

    # import binascii
    # result2 = binascii.hexlify(result2)
    
    # print(result2)

    # print(result2.decode("ascii"))#

    # write_on_file('example2.txt', result2, 'wb')

    # cifrar com OAEP e assinar são coisas diferentes

    # assinar = cryptografar com RSA (usando chave privada) o hash do arquivo (sha3)
    '''