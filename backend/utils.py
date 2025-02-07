import requests

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return n == sum(d ** len(digits) for d in digits)

def get_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}")
        return response.text
    except:
        return "No fun fact available."

def classify_number(n):
    properties = []
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    if is_armstrong(n):
        properties.append("armstrong")

    return {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": is_perfect(n),
        "properties": properties,
        "digit_sum": sum(map(int, str(n))),
        "fun_fact": get_fun_fact(n)
    }
