"""
Auto-generated task-level solver.

Task ID: Task_3_13
Task Type: 6_Ranking
Task Description: Identify which service instance is called most frequently in a given trace.
Question Template: Which service instance is called most frequently in the Input Trace?
"""

from collections import defaultdict
from typing import List

def solution(trace1: List[dict]) -> List[str]:
    service_counts = defaultdict(int)
    for span in trace1:
        service_counts[span['service.name']] += 1
    max_count = max(service_counts.values())
    return [service for service, count in service_counts.items() if count == max_count]
