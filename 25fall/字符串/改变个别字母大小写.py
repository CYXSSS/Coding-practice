a = str(input("请输入一个字符串："))
b = ''
for char in a:
    if char in {'e','r','n'}:
        char = char.upper()
    if char in {'M','I','K','A','S'}:
        char = char.lower()
    b += char
print(b)
# 字符串的重新赋值：单独字符串不可重新赋值！