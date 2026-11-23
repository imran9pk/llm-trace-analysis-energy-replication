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
    frequency = defaultdict(int)
    for span in trace1:
        frequency[span['name']] += 1
    max_frequency = max(frequency.values())
    return [name for name, count in frequency.items() if count == max_frequency]
