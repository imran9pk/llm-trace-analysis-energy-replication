"""
Auto-generated task-level solver.

Task ID: Task_3_12
Task Type: 6_Ranking
Task Description: Identify which service is called most frequently in a given trace.
Question Template: Which service is called most frequently in the Input Trace?
"""

def solution(trace1):
    from collections import Counter

    service_calls = [span['service.name'] for span in trace1]
    service_counter = Counter(service_calls)
    max_count = max(service_counter.values())
    most_frequent_services = [service for service, count in service_counter.items() if count == max_count]

    return most_frequent_services
