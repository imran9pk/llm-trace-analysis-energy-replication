"""
Auto-generated task-level solver.

Task ID: Task_3_18
Task Type: 6_Ranking
Task Description: Identify which database is accessed most frequently in a given trace.
Question Template: Which database is accessed most frequently in the Input Trace?
"""

from collections import defaultdict
from typing import List, Dict

def solution(trace1: List[Dict]) -> List[str]:
    db_access_count = defaultdict(int)
    for span in trace1:
        if 'db' in span['name']:
            db_access_count[span['name']] += 1
    max_count = max(db_access_count.values())
    return [db for db, count in db_access_count.items() if count == max_count]
