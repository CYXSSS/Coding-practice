def myAtoi(s):
    s = s.strip()  # Remove leading whitespace
    s_list = list(s)
    a = {'sign': ''} # Initialize dictionary
    if s_list[0] == '-' or s_list[0] == '+':
        a['sign'] = s_list[0]
        s_list = s_list[1:]
        for char in s_list:
            if s_list[0] == 0:
                s_list = s_list[1:]
            if char.isdigit() == False:
                break
            if char.isdigit():
                a['num'] = a.get('num', '') + char
            if a['num'] == None:
                a['num'] = '0'           
    else:
        for char in s_list:
            if s_list[0] == 0:
                s_list = s_list[1:]
            if char.isdigit() == False:
                break
            if char.isdigit():
                a['num'] = a.get('num', '') + char
            if a.get('num') == None:
                a['num'] = '0'            
    if a['sign'] == '-':
        a['num'] = '-' + a.get('num', '0')
    else:
        a['num'] = a.get('num', '0')
    final_value = int(a['num'])
    return final_value                    
print(myAtoi("words and 987"))  # Example usage
            
                

            
        


       
         