def selectionsorting(arr):
    n = len(arr)
    for i in range(n-1):
        min_idx = i
        swapped = False
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swapped = True
        if not swapped:
            break
    return arr

def recrusive_selection_sort(arr, start=0):
    if start >= len(arr) - 1:
        return arr
    min_idx = start
    for i in range(start + 1, len(arr)):
        if arr[i] < arr[min_idx]:
            min_idx = i
            arr[start], arr[min_idx] = arr[min_idx], arr[start]
    return recrusive_selection_sort(arr, start + 1)

# Example usage:
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(selectionsorting(arr))

# All cases(original version): T(n) = O(n^2)
# Best case(Optimized version): T(n) = O(n)
# S(n) = O(1) as it is an in-place sorting algorithm
# Not Stable