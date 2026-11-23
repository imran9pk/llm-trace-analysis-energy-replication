"""
Auto-generated task-level solver.

Task ID: Task_3_13
Task Type: 6_Ranking
Task Description: Identify which service instance is called most frequently in a given trace.
Question Template: Which service instance is called most frequently in the Input Trace?
"""

from collections import defaultdict
from typing import List, Dict

def solution(trace1: List[Dict]) -> List[str]:
    frequency = defaultdict(int)
    for span in trace1:
        frequency[span['service.name']] += 1

    max_frequency = max(frequency.values())
    most_frequent_services = [service for service, count in frequency.items() if count == max_frequency]

    return most_frequent_services
