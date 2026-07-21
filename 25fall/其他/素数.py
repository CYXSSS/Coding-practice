def is_prime(n):
    """判断一个数是否为质数"""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # 如果有一个大于n^0.5的根，那么必定有一个小于n^0.5的根
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

num = int(input("请输入一个正整数: "))
while True:
    num += 1
    if is_prime(num):
        print(f"下一个质数是: {num}")
        break
    
        
       
    



	
      

