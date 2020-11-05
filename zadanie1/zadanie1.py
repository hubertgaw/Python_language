# Martyna Piasecka 224398
# Hubert Gawłowski 224298

# 3.1 Approximation


def approximation(n):
    product = 1.0
    for i in range(1, n):
        numerator = (2 * i) * (2 * i)
        denominator = (2 * i - 1) * (2 * i + 1)
        product *= numerator / denominator
        # print(product * 2)
        print("Przyblizenie nr.", i, "=", product * 2)


approximation(11)


# 3.2 NWD

def nwd(a, b):
    while b != 0:
        # mod = rest of the division
        c = a % b
        a = b
        b = c
    return a


a = 84
b = 18
print("\nNajwiekszy wspolny dzielnik liczb", a, "oraz", b, "to", nwd(a, b))


# 4 Eratostenes sieve

def eratostenes_sieve(koniec):
    sito = []
    # filling the list with true
    for i in range(0, koniec + 1, 1):
        sito.append(1)

    # enumeration of prime numbers
    for i in range(2, koniec + 1, 1):
        # if dealing with true
        if sito[i] == 1:
            cos = i * i
            # check the multiples
            while cos < koniec:
                # change the multiples to false and increase 'cos'
                sito[cos] = 0
                cos += i

    # prime number display, begin with index [2]
    liczby_pierwsze = []
    for i in range(2, koniec, 1):
        # if true, add to the new list
        if sito[i] == 1:
            liczby_pierwsze.append(i)
    print("\nLiczby pierwsze: ", liczby_pierwsze)


k = 100
eratostenes_sieve(k)


# 5 The smallest common multiple
def prime_factors(x):
    factors = []
    while x > 1:
        for i in range(2, x + 1):
            if x % i == 0:
                factors.append(i)
                x = int(x / i)
                break
    return factors


def smallest_common_multiple(a, b):
    result = 1
    factors1 = prime_factors(a)
    factors2 = prime_factors(b)
    factors1_set = set(factors1)
    factors2_set = set(factors2)
    for i in factors1_set:
        if i in factors2_set:
            x = factors1.count(i)
            y = factors2.count(i)
            if x > y:
                result *= i ** x
            else:
                result *= i ** y
        else:
            result *= i
    for i in factors2_set:
        if i not in factors1_set:
            result *= i
    return result


x = 192
y = 348
print("NWW dla 192 i 348 to: ", smallest_common_multiple(x, y))
