def bubblesorting(arr):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n-1):
        # Last i elements are already sorted
        swapped = False
        for j in range(0, n-i-1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # If no two elements were swapped by inner loop, then break
        if not swapped:
            break
    return arr

# T(n) = O(n^2) in worst and average case
# T(n) = O(n) in best case (when the array is already sorted)
# S(n) = O(1) as it is an in-place sorting algorithm
# Stable
