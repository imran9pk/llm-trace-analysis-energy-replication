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
    span_ids = set()

    for span in trace1:
        span_ids.add(span['spanId'])

    for span in trace1:
        if span['spanId'] in span_ids:
            operation_counts[span['name']] += 1

    max_count = max(operation_counts.values()) if operation_counts else 0
    return [op for op, count in operation_counts.items() if count == max_count]
