"""
Auto-generated task-level solver.

Task ID: Task_3_14
Task Type: 6_Ranking
Task Description: Identify which operation is executed most frequently in a given trace.
Question Template: Which operation is executed most frequently in the Input Trace?
"""

from collections import defaultdict
from typing import List

def solution(trace1: List[dict]) -> List[str]:
    span_count = defaultdict(int)
    for span in trace1:
        span_count[span['name']] += 1
    max_count = max(span_count.values())
    return [name for name, count in span_count.items() if count == max_count]
