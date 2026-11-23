"""
Auto-generated task-level solver.

Task ID: Task_3_12
Task Type: 6_Ranking
Task Description: Identify which service is called most frequently in a given trace.
Question Template: Which service is called most frequently in the Input Trace?
"""

def solution(trace1):
    from collections import defaultdict

    service_counts = defaultdict(int)
    span_ids = set()
    parent_span_ids = set()

    for span in trace1:
        span_ids.add(span['spanId'])
        parent_span_id = span['parentSpanId']
        if parent_span_id != -1:
            parent_span_ids.add(parent_span_id)

    for span in trace1:
        if span['spanId'] in parent_span_ids:
            service_counts[span['service.name']] += 1

    max_count = max(service_counts.values()) if service_counts else 0
    return [service for service, count in service_counts.items() if count == max_count]
