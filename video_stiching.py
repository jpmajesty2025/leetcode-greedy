"""
You are given a series of video clips from a sporting event that lasted time seconds. These video clips 
can be overlapping with each other and have varying lengths.

Each video clip is described by an array clips where clips[i] = [starti, endi] indicates that the ith 
clip started at starti and ended at endi.

We can cut these clips into segments freely.

For example, a clip [0, 7] can be cut into segments [0, 1] + [1, 3] + [3, 7].
Return the minimum number of clips needed so that we can cut the clips into segments that cover the entire 
sporting event [0, time]. If the task is impossible, return -1.
"""

def video_stitching(clips: list[list[int]], time: int) -> int:
    """Return the minimum number of clips needed to cover the entire sporting event [0, time].

    If the task is impossible, return -1. The input is not modified.

    Raises ValueError if time is negative.
    """
    if time < 0:
        raise ValueError("time must be non-negative.")

    # Sort a copy by start time so the caller's list keeps its order
    clips = sorted(clips, key=lambda clip: clip[0])

    count = 0
    current_end = 0
    next_end = 0
    i = 0
    n = len(clips)

    while current_end < time:
        while i < n and clips[i][0] <= current_end:
            next_end = max(next_end, clips[i][1])
            i += 1

        if next_end == current_end:
            return -1  # No further progress can be made

        count += 1
        current_end = next_end

    return count
