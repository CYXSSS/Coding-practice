def merge_sort_recursive(arr):
    # 基本情况：如果数组长度小于等于1，直接返回（已经是天然有序的）
    if len(arr) <= 1:
        return arr
    
    # 1. 分（Divide）：找到中点，将数组分为左右两半
    mid = len(arr) // 2
    left_half = merge_sort_recursive(arr[:mid])
    right_half = merge_sort_recursive(arr[mid:])
    
    # 2. 治与合（Conquer & Merge）：合并两个已排序的子数组
    return merge(left_half, right_half)

def merge(left, right):
    result = []
    i, j = 0, 0
    
    # 比较左右数组的元素，将较小的依次放入结果数组
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    # 如果左/右数组还有剩余元素，直接追加到结果数组末尾
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result



def merge_sort_iterative(arr):
    n = len(arr)
    if n <= 1:
        return arr
    
    # width 表示每次合并的子数组的长度，初始为 1
    width = 1
    
    # 当子数组长度小于总长度时，继续成倍扩大并合并
    while width < n:
        # i 是每次合并操作的起始索引
        # 每次步进 2 * width，因为我们要合并两个长度为 width 的区间
        for i in range(0, n, 2 * width):
            # 确定左右子数组的边界
            left = i
            mid = min(i + width, n)       # 防止越界：右子数组的起始点
            right = min(i + 2 * width, n) # 防止越界：右子数组的终点
            
            # 合并 arr[left:mid] 和 arr[mid:right]
            merged = []
            l, r = left, mid
            
            while l < mid and r < right:
                if arr[l] <= arr[r]:
                    merged.append(arr[l])
                    l += 1
                else:
                    merged.append(arr[r])
                    r += 1
                    
            while l < mid:
                merged.append(arr[l])
                l += 1
            while r < right:
                merged.append(arr[r])
                r += 1
                
            # 将合并好的局部有序数组替换回原数组的对应位置
            arr[left:right] = merged
            
        # 这一轮合并完毕，子数组长度翻倍
        width *= 2
        
    return arr


# T(n) = O(nlog n)  # 时间复杂度
# S(n) = O(n)       # 空间复杂度（递归调用栈和合并结果数组的空间）