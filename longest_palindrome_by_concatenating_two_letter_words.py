"""
You are given an array of strings words. Each element of words consists of two lowercase English letters.

Create the longest possible palindrome by selecting some elements from words and concatenating them in any order. 
Each element can be selected at most once.

Return the length of the longest palindrome that you can create. If it is impossible to create any palindrome, 
return 0.

A palindrome is a string that reads the same forward and backward.
"""

from typing import Counter


def longest_palindrome(words: list[str]) -> int:    
    # Count the frequency of each two-letter word
    count = Counter(words)
    
    length = 0
    has_center = False
    
    for word, freq in count.items():
        if word[0] == word[1]:  # Check if the word is a palindrome (e.g., "aa", "bb")
            length += (freq // 2) * 4  # Each pair contributes 4 to the length
            if freq % 2 == 1:
                has_center = True  # We can use one of these as the center of the palindrome
        else:
            reverse_word = word[::-1]
            if reverse_word in count:
                pairs = min(freq, count[reverse_word])
                length += pairs * 4  # Each pair contributes 4 to the length
                count[reverse_word] -= pairs  # Decrease the count of the reverse word to avoid double counting
    
    if has_center:
        length += 2  # Add one center character if available
    
    return length