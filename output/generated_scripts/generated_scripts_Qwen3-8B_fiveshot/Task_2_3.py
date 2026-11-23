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
    graph = defaultdict(list)
    services = set()
    for span in trace1:
        service_name = span['service.name']
        services.add(service_name)
        parent_span_id = span['parentSpanId']
        if parent_span_id != '-1':
            # Only consider HTTP calls (client or server spans)
            if span['kind'] in ['SPAN_KIND_CLIENT', 'SPAN_KIND_SERVER']:
                graph[service_name].append(span['service.name'])

    # Check for a path from key_component_1 to key_component_2 using BFS
    visited = set()
    queue = [(key_component_1, 0)]
    while queue:
        current_service, depth = queue.pop(0)
        if current_service == key_component_2:
            return 'Yes'
        if current_service in visited:
            continue
        visited.add(current_service)
        for neighbor in graph[current_service]:
            if neighbor not in visited:
                queue.append((neighbor, depth + 1))
    return 'No'
