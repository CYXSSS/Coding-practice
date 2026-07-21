def insertsorting(arr):
    n = len(arr)
    for i in range(n-1):
        # n-1: because the last element will already be in place after the second to last iteration
        j = i + 1
        key = arr[j]
        while j > 0 and arr[j-1] > key:
            arr[j] = arr[j-1]
            j -= 1
            arr[j] = key
    return arr
# Example usage
arr = [2,3,8,7,1,2,2,2,7,3,9,8,2,1,4,2,4,6,9,2]
print(insertsorting(arr))
# Worst case: T(n) = O(n^2)
# Best case: T(n) = O(n) 
# S(n) = O(1) for the in-place version,
# S(n) = O(n) for the version that creates a new array
# Stable