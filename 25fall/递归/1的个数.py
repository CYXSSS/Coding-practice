def count_digit_one(n):
    if n < 1:
        return 0  # 基准情况：n小于1时没有1
    
    # 计算n的位数、最高位、最高位的位因子（10^(d-1)）
    d = len(str(n))  # 位数
    power = 10 **(d - 1)  # 最高位的位因子（如314的power=100）
    high = n // power  # 最高位数字（如314的high=3）
    rest = n % power  # 剩余部分（如314的rest=14）
    
    # 情况1：0 ~ power-1 中1的个数（递归计算）
    count = count_digit_one(power - 1)
    
    # 情况2：power ~ high*power - 1 中1的个数
    if high > 1:
        # 最高位为1的次数：power次（如100~199的百位有100个1）
        count += power
    elif high == 1:
        # 最高位为1的次数：rest + 1次（如100~114的百位有15个1）
        count += rest + 1
    # 低位的1的个数：high * 情况1的次数（每一段低位都对应0~power-1的情况）
    count += high * count_digit_one(power - 1)
    
    # 情况3：high*power ~ n 中1的个数（递归计算剩余部分）
    count += count_digit_one(rest)
    
    return count