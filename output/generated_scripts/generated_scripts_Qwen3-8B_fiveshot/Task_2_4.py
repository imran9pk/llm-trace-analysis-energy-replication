"""
Auto-generated task-level solver.

Task ID: Task_2_4
Task Type: 3_Existence
Task Description: Determine whether a service instance call path from a source service instance to a destination service instance exists in a given trace.
Question Template: Is there an HTTP call path from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    from collections import defaultdict

    # Build a graph of service instances
    graph = defaultdict(list)
    service_to_host = {}
    for span in trace1:
        service_name = span['service.name']
        host_name = span['host.name']
        service_to_host[service_name] = host_name

    # Build the graph based on parent-child relationships
    for span in trace1:
        parent_span_id = span['parentSpanId']
        if parent_span_id == '-1':
            continue
        parent_service_name = None
        for s in trace1:
            if s['spanId'] == parent_span_id:
                parent_service_name = s['service.name']
                break
        if parent_service_name is None:
            continue
        child_service_name = span['service.name']
        graph[parent_service_name].append(child_service_name)

    # Check for a path from key_component_1 to key_component_2
    visited = set()
    queue = [key_component_1]
    while queue:
        current = queue.pop(0)
        if current == key_component_2:
            return 'Yes'
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph.get(current, []):
            queue.append(neighbor)
    return 'No'
