def countsorting(arr):
    if not arr:
        return []

    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    sorted_arr = []
    for i, cnt in enumerate(count):
        sorted_arr.extend([i] * cnt)

    return sorted_arr

arr = [2,3,8,7,1,2,2,2,7,3,9,8,2,1,4,2,4,6,9,2]
print(countsorting(arr))

# T(n) = O(n + k) where n is the number of elements in input array and k is the range of the input
# S(n) = O(k) for the count array
# Stable