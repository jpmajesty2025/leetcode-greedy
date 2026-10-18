"""
Video Stitching: Furthest-Reach Array (Jump Game Style, No Sorting).

1. Build reach[s] = the furthest end of any clip that starts at s, for s in 0..time. A clip that
   starts before 0 is treated as starting at 0, and a clip that starts after time is irrelevant.
2. Sweep positions 0..time-1 once, tracking the furthest point any clip seen so far can reach.
3. Each time the sweep arrives at the end of the current segment, we must commit to one more clip:
   take the furthest-reaching one. If it reaches no further than where we stand, there is a gap: -1.

This is the same greedy as the sorted version, but bucketing by start time replaces the sort.
It is faster when time is small compared to the number of clips.

Time Complexity: O(n + time)
Space Complexity: O(time)
"""


def video_stitching(clips: list[list[int]], time: int) -> int:
    """Return the minimum number of clips needed to cover the entire sporting event [0, time].

    If the task is impossible, return -1. The input is not modified.

    Raises ValueError if time is negative.
    """
    if time < 0:
        raise ValueError("time must be non-negative.")

    reach = [0] * (time + 1)
    for start, end in clips:
        start = max(start, 0)
        if start <= time and end > reach[start]:
            reach[start] = end

    count = 0
    segment_end = 0  # end of the area covered by the clips chosen so far
    furthest = 0     # furthest point reachable with one more clip
    for position in range(time):
        furthest = max(furthest, reach[position])
        if position == segment_end:
            if furthest <= position:
                return -1  # nothing starts at or before here and reaches past here
            count += 1
            segment_end = furthest
            if segment_end >= time:
                break
    return count
