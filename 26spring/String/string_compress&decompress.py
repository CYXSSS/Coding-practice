def compress(text):
    if not text: return ""
    
    res = []
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i-1]:
            count += 1
        else:
            res.append(text[i-1] + str(count))
            count = 1
    res.append(text[-1] + str(count))
    
    compressed = "".join(res)
    return compressed if len(compressed) < len(text) else text

def decompress(text):
    res = []
    i = 0
    while i < len(text):
        char = text[i]
        count_str = ""
        i += 1
        while i < len(text) and text[i].isdigit():
            count_str += text[i]
            i += 1
        res.append(char * int(count_str))
    return "".join(res)

# 测试
s = "AAAABBBCCDAA"
compressed = compress(s)
print(f"压缩: {compressed}")   # A4B3C2D1A2
print(f"解压: {decompress(compressed)}")

