def binary_search_with_upper_bound(arr, target):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        mid = (low + high) // 2
        iterations += 1

        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            upper_bound = arr[mid] 
    
    if upper_bound is None:
        if low < len(arr):
            upper_bound = arr[low]
        else:
            upper_bound = None 

    return (iterations, upper_bound)


sorted_array = [0.1, 1.2, 3.4, 4.5, 6.7, 8.9]
target = 4.5
result = binary_search_with_upper_bound(sorted_array, target)
print(result) 
