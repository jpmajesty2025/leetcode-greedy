"""
You have some apples and a basket that can carry up to 5000 units of weight.

Given an integer array weight where weight[i] is the weight of the ith apple, return the maximum number of apples 
you can put in the basket.
"""

def max_number_of_apples(weight: list[int]) -> int:
    # Sort the weights of the apples in ascending order
    weight.sort()
    
    total_weight = 0
    count = 0
    
    for w in weight:
        if total_weight + w <= 5000:
            total_weight += w
            count += 1
        else:
            break
    
    return count