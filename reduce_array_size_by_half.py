"""
You are given an integer array arr. You can choose a set of integers and remove all the occurrences of these 
integers in the array.

Return the minimum size of the set so that at least half of the integers of the array are removed.
"""

def min_set_size(self, arr: list[int]) -> int:
    from collections import Counter
    
    # Count the frequency of each integer in the array
    count = Counter(arr)
    
    # Get the frequencies sorted in descending order
    frequencies = sorted(count.values(), reverse=True)
    
    total_removed = 0
    set_size = 0
    half_length = len(arr) // 2
    
    for freq in frequencies:
        total_removed += freq
        set_size += 1
        if total_removed >= half_length:
            break
            
    return set_size