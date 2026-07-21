nums = [int(x.strip()) for x in input('请输入一串整数：').split(',')]
target = int(input('请输入一个整数'))
def twosum(nums: list, target: int) -> list[int]:
    n = len(nums)
    for i in range(n):
        for j in range(i+1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
two_sum = twosum(nums, target)
print(two_sum)


