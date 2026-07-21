def findRepeatedDnaSequences(s):
    start = 0
    end = 9
    count = {}
    for end in range(9, len(s)):
        substr = s[start:end+1] 
        if substr not in count:
            count[substr] = 1 #易忘：初始化为1
        else:
            count[substr] = count[substr] + 1
        start += 1
    max_count = max(count.values()) #max()不能一次表示多个等大值，要分两步进行
    max_keys = [k for k, v in count.items() if v == max_count] 
    return max_keys
s = str(input("请输入一串长度大于十的DNA序列: "))
print(findRepeatedDnaSequences(s))
        

                

            
               