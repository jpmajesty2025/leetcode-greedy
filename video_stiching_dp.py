"""
Video Stitching: Dynamic Programming Over Time.

1. dp[t] = the minimum number of clips needed to cover [0, t]; dp[0] = 0.
2. A clip [s, e] with s < t <= e can finish the cover of [0, t] after the cover of [0, s]:
   dp[t] = min(dp[s] + 1) over such clips.
3. dp[time] is the answer, or -1 if it stayed unreachable.

Slower than the greedy versions, but it makes no greedy argument at all: it is a direct recurrence,
so it is easy to trust and works well as a cross-check.

Time Complexity: O(n * time)
Space Complexity: O(time)
"""


def video_stitching(clips: list[list[int]], time: int) -> int:
    """Return the minimum number of clips needed to cover the entire sporting event [0, time].

    If the task is impossible, return -1. The input is not modified.

    Raises ValueError if time is negative.
    """
    if time < 0:
        raise ValueError("time must be non-negative.")

    # Integer sentinel keeps dp a list[int]. A minimal cover never uses a clip twice, so any real
    # answer is at most len(clips); one more than that can only mean "unreachable".
    unreachable = len(clips) + 1
    dp: list[int] = [unreachable] * (time + 1)
    dp[0] = 0
    for t in range(1, time + 1):
        for start, end in clips:
            start = max(start, 0)
            if start < t <= end and dp[start] + 1 < dp[t]:
                dp[t] = dp[start] + 1
    return -1 if dp[time] == unreachable else dp[time]
