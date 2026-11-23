"""
Auto-generated task-level solver.

Task ID: Task_3_12
Task Type: 6_Ranking
Task Description: Identify which service is called most frequently in a given trace.
Question Template: Which service is called most frequently in the Input Trace?
"""

def solution(trace1):
    service_counts = {}
    for span in trace1:
        service_name = span['service.name']
        service_counts[service_name] = service_counts.get(service_name, 0) + 1
    max_count = max(service_counts.values())
    return [service for service, count in service_counts.items() if count == max_count]
