import random 

FIRST_PRIMES_LIST = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                     31, 37, 41, 43, 47, 53, 59, 61, 67,  
                     71, 73, 79, 83, 89, 97, 101, 103,  
                     107, 109, 113, 127, 131, 137, 139,  
                     149, 151, 157, 163, 167, 173, 179,  
                     181, 191, 193, 197, 199, 211, 223, 
                     227, 229, 233, 239, 241, 251, 257, 
                     263, 269, 271, 277, 281, 283, 293, 
                     307, 311, 313, 317, 331, 337, 347, 349] 
  
NUMBER_OF_TRIES = 20

def random_n_bits_number(n): 
    return random.randrange(2 ** (n-1) + 1, 2 ** n - 1) 
  
def low_level_prime(n): 
		while True: 
				prime_candidate = random_n_bits_number(n)  
				for divisor in FIRST_PRIMES_LIST: 
						if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate: 
								break
				else:
					return prime_candidate

def trial_composite(round_tester, even_component, prime_candidate, max_divisions_by_two): 
		if pow(round_tester, even_component, prime_candidate) == 1: 
				return False
		for i in range(max_divisions_by_two): 
				if pow(round_tester, 2**i * even_component, prime_candidate) == prime_candidate-1: 
						return False
		return True

def miller_rabin(prime_candidate): 
    max_divisions_by_two = 0
    even_component = prime_candidate-1

    while even_component % 2 == 0: 
        even_component >>= 1
        max_divisions_by_two += 1
    assert(2 ** max_divisions_by_two * even_component == prime_candidate-1) 
  
    for _ in range(NUMBER_OF_TRIES): 
        round_tester = random.randrange(2, prime_candidate) 
        if trial_composite(round_tester, even_component, prime_candidate, max_divisions_by_two): 
            return False
    return True

def get_prime_128_bits():
		prime = 0
		while True: 
				n = 1024
				prime_candidate = low_level_prime(n) 
				if not miller_rabin(prime_candidate): 
						continue
				else: 
						prime = prime_candidate
						break
		return prime