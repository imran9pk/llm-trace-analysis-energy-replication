"""
Auto-generated task-level solver.

Task ID: Task_2_3
Task Type: 3_Existence
Task Description: Determine whether a service call path from a source service to a destination service exists in a given trace.
Question Template: Is there an HTTP call path from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    from collections import defaultdict

    # Build a graph of service calls
    graph = defaultdict(set)
    spans = trace1
    span_ids = {}
    for span in spans:
        span_ids[span['spanId']] = span

    for span in spans:
        if span['parentSpanId'] != -1:
            parent_span = span_ids[span['parentSpanId']]
            if parent_span['service.name'] == key_component_1 and span['service.name'] == key_component_2:
                graph[key_component_1].add(key_component_2)
                break

    # Check if there's a path from key_component_1 to key_component_2
    visited = set()
    queue = [key_component_1]
    while queue:
        current = queue.pop(0)
        if current == key_component_2:
            return "Yes"
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            queue.append(neighbor)

    return "No"
