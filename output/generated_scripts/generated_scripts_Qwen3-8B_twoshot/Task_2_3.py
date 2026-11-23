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
    for span in trace1:
        service_name = span['service.name']
        parent_span_id = span['parentSpanId']
        if parent_span_id == '-1':
            continue  # Skip root span as it has no parent
        # Find the parent span to determine the caller
        parent_span = next((s for s in trace1 if s['spanId'] == parent_span_id), None)
        if parent_span:
            parent_service = parent_span['service.name']
            graph[parent_service].add(service_name)

    # Check for a path from key_component_1 to key_component_2 using BFS
    visited = set()
    queue = [key_component_1]
    while queue:
        current = queue.pop(0)
        if current == key_component_2:
            return 'Yes'
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            queue.append(neighbor)
    return 'No'
