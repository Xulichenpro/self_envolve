import random
import math

# Pollard's Rho 算法分解大整数
def pollards_rho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        x = random.randrange(2, n - 1)
        y = x
        c = random.randrange(1, n - 1)
        d = 1

        f = lambda x: (pow(x, 2, n) + c) % n

        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)

            if d == n:
                break
        if d > 1 and d < n:
            return d

# 递归分解
def factor(n):
    if n == 1:
        return []
    if is_prime(n):
        return [n]
    d = pollards_rho(n)
    return factor(d) + factor(n // d)

# Miller-Rabin 素性测试
def is_prime(n):
    if n < 2:
        return False
    for p in [2,3,5,7,11,13,17,19,23]:
        if n % p == 0:
            return n == p

    # write n-1 = d * 2^s
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def discription() -> dict:
    tool = {
        "type": "function",
        "function": {
            "name": "factor",
            "description": "分解大整数",
            "parameters": {
                "type": "object",
                "properties": {
                    "N": {
                        "type": "integer",
                        "description": "需要分解的大整数"
                    }
                },
                "required": ["N"]
            }
        }   
    }
    return tool

def tool_call(N:int):
    return factor(N)



# 示例
if __name__ == "__main__":
    N = int(input("Enter N to factor: "))
    print("Factors:", factor(N))
