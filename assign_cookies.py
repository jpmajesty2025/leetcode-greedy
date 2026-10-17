"""
Assume you are an awesome parent and want to give your children some cookies. But, you should 
give each child at most one cookie.

Each child i has a greed factor g[i], which is the minimum size of a cookie that the child will 
be content with; and each cookie j has a size s[j]. If s[j] >= g[i], we can assign the cookie j 
to the child i, and the child i will be content. Your goal is to maximize the number of your 
content children and output the maximum number.
"""

def find_content_children(g: list[int], s: list[int]) -> int:
    # Sort the greed factors and cookie sizes
    g.sort()
    s.sort()
    
    child_i = 0  # Pointer for children
    cookie_j = 0  # Pointer for cookies
    
    while child_i < len(g) and cookie_j < len(s):
        if s[cookie_j] >= g[child_i]:  # If the cookie can satisfy the child's greed
            child_i += 1  # Move to the next child
        cookie_j += 1  # Move to the next cookie
    
    return child_i  # The number of content children