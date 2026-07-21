def binarysearch(arr, target):
    n = len(arr)
    low = 0
    high = n - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
# Example usage
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 5
result = binarysearch(arr, target)
if result != -1:
    print(f"Element found at index: {result}")
else:
    print("Element not found in the array.")

def bs_recursive(arr, target, low, high):
    n = len(arr)
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        return bs_recursive(arr, target, mid + 1, high)
    else:
        return bs_recursive(arr, target, low, mid - 1)
# Example usage
arr = [1, 2, 3, 4, 5, 6 , 7, 8, 9]
target = 5
result = bs_recursive(arr, target, 0, len(arr) - 1)
print(f"Element found at index: {result}")

# All cases: T(n) = O(logn)