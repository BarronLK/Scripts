def check_id_length(n):  # 判断身份证号长度是否正确
    if len(str(n)) != 18:
        return False
    else:
        return True
def check_id_data(n):  # 检查数据
    factor = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    last = ("1", "O", "X", "9", "8", "7", "6", "5", "4", "3", "2")
    n = str(n)
    sum = 0
    for i in range(0, 17):
        sum += int(n[i]) * factor[i]  # 求前17位与加权数相乘的和
    sum %= 11  # 取余，计算余数对应的第18位身份证号
    if (last[sum]) == str(n[17]):  # 第18位相同
        print("身份证号规则校验通过，校验码是:"+str(last[sum]))
        return sum
    else:
        print("当前身份证号校验失败，校验码应为:"+str(last[sum]))
        return 0
n = input("请输入18位身份证号:")
if check_id_length(n):
    check_id_data(n)
else:
    print("身份证号位数不正确,请重新输入!")