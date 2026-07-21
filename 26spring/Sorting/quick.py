def quick_sort_simple(arr):
    if len(arr) <= 1:
        return arr
    
    # 选择中间元素作为基准值 (Pivot)
    pivot = arr[len(arr) // 2]
    
    # 将数组分为三部分
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # 递归排序左边和右边，最后拼接
    return quick_sort_simple(left) + middle + quick_sort_simple(right)


def quick_sort_inplace(arr, low, high):
    if low < high:
        # 获取分区索引
        pivot_index = partition(arr, low, high)
        # 递归排序左子数组
        quick_sort_inplace(arr, low, pivot_index - 1)
        # 递归排序右子数组
        quick_sort_inplace(arr, pivot_index + 1, high)

def partition(arr, low, high):
    # 选择最右边的元素作为基准
    pivot = arr[high]
    i = low  # i 指向小于等于基准的元素的最后一个位置
    
    for j in range(low, high):
        # 如果当前元素小于或等于基准
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1 
            
    # 最后把基准元素换到中间位置 i
    arr[i], arr[high] = arr[high], arr[i]
    return i


# T(n) = O(nlog n) 平均时间复杂度
# T(n) = O(n^2) 最坏时间复杂度（当输入数组已经有序或逆序时）
# S(n) = O(log n) in-place 版本的空间复杂度，因为递归调用栈的深度为 log n
# S(n) = O(n) simple 版本的空间复杂度，因为创建了新的列表

