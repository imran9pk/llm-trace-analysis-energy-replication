"""
Auto-generated task-level solver.

Task ID: Task_3_16
Task Type: 6_Ranking
Task Description: Identify which type of SQL statement is executed most frequently in a given trace.
Question Template: Which type of SQL statement is executed most frequently in the Input Trace?
"""

from collections import defaultdict

def solution(trace1):
    sql_types = defaultdict(int)
    for span in trace1:
        if 'db.operation' in span:
            sql_types[span['db.operation']] += 1
    max_count = max(sql_types.values())
    return [key for key, value in sql_types.items() if value == max_count]
