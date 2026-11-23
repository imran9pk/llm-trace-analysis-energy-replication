"""
Auto-generated task-level solver.

Task ID: Task_3_17
Task Type: 6_Ranking
Task Description: Identify which table is accessed most frequently in a given trace.
Question Template: Which table is accessed most frequently in the Input Trace?
"""

from collections import defaultdict
from typing import List, Dict

def solution(trace1: List[Dict]) -> List[str]:
    table_access_count = defaultdict(int)
    for span in trace1:
        if 'attributes' in span and 'db.statement' in span['attributes']:
            table_access_count[span['attributes']['db.statement']] += 1
    max_count = max(table_access_count.values())
    return [table for table, count in table_access_count.items() if count == max_count]
