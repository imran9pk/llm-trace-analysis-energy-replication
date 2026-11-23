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
    graph = defaultdict(set)
    for span in trace1:
        parent_span_id = span['parentSpanId']
        span_id = span['spanId']
        service_name = span['service.name']
        host_name = span['host.name']
        if parent_span_id != '-1':
            # If the span has a parent, it's a child span
            # Check if the parent is a server span (caller)
            if span['kind'] == 'SPAN_KIND_CLIENT':
                # This span is a client, so it's a call from the parent to this span
                graph[host_name].add(service_name)
            elif span['kind'] == 'SPAN_KIND_SERVER':
                # This span is a server, so it's a call from this span to the parent
                graph[service_name].add(host_name)
    
    # Check if there's a path from key_component_1 to key_component_2
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
