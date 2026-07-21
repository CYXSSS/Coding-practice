def isPowerOfTwo(n: int) -> bool:
    if n <= 0:
        return False
    elif n == 1:
        return True
    elif n % 2 != 0:
        return False
    else:
        return isPowerOfTwo(n / 2)
print(isPowerOfTwo(16))
    