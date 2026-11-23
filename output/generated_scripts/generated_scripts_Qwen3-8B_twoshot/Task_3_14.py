"""
Auto-generated task-level solver.

Task ID: Task_3_14
Task Type: 6_Ranking
Task Description: Identify which operation is executed most frequently in a given trace.
Question Template: Which operation is executed most frequently in the Input Trace?
"""

def solution(trace1):
    from collections import defaultdict

    operation_counts = defaultdict(int)
    for span in trace1:
        operation_counts[span['name']] += 1

    max_count = max(operation_counts.values())
    result = [op for op, count in operation_counts.items() if count == max_count]
    return result
