def compare(a, b):
    if a == b:
        return 0
    elif a > b:
        return a-b
    else:
        return b-a
def days_in_month(year, month_of_year):
    if month_of_year in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month_of_year in [4, 6, 9, 11]:
        return 30
    elif month_of_year == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return 29
        else:
            return 28
    else:
        return "Invalid month"
a_list = list(map(int, input('请输入年-月-日：').split('-')))
b_list = list(map(int, input('请输入年-月-日：').split('-')))
if a_list[0] == b_list[0]:
    if a_list[1] == b_list[1]:
        print('相差天数为：', compare(a_list[2], b_list[2]), '天')
    else:
        days_Delta = 0
        if a_list[1] > b_list[1]:
            for month in range(b_list[1]+1, a_list[1]):
                days_Delta += days_in_month(a_list[0], month)
            day_delta = days_in_month(b_list[0], b_list[1]) - b_list[2] + a_list[2] + days_Delta
        else:
            for month in range(a_list[1]+1, b_list[1]):
                days_Delta += days_in_month(a_list[0], month)
            day_delta = days_in_month(a_list[0], a_list[1]) - a_list[2] + b_list[2] + days_Delta
            print('相差天数为：', day_delta, '天')
elif a_list[0] != b_list[0]:
    print('年份不一样，计算复杂，程序不支持')
            
            




       