memo = {0: 0, 1: 1}
def fib(n):
    """Return the nth Fibonacci number."""
    if n in memo:
        return memo[n]
    
    # 终止条件
    if n <= 1:
        return n
    value = fib(n - 1) + fib(n - 2)
    memo[n] = value
    return value
print(fib(80))
