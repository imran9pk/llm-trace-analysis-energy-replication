"""
Auto-generated task-level solver.

Task ID: Task_2_3
Task Type: 3_Existence
Task Description: Determine whether a service call path from a source service to a destination service exists in a given trace.
Question Template: Is there an HTTP call path from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    from collections import defaultdict, deque

    # Build a graph of service calls
    graph = defaultdict(list)
    service_to_spans = defaultdict(list)
    
    for span in trace1:
        service_name = span['service.name']
        service_to_spans[service_name].append(span)
    
    # Build the graph based on parent-child relationships
    for span in trace1:
        span_id = span['spanId']
        parent_span_id = span['parentSpanId']
        if parent_span_id != '-1':
            parent_span = next((s for s in trace1 if s['spanId'] == parent_span_id), None)
            if parent_span:
                parent_service = parent_span['service.name']
                child_service = span['service.name']
                graph[parent_service].append(child_service)
    
    # BFS to check if there's a path from key_component_1 to key_component_2
    visited = set()
    queue = deque([key_component_1])
    visited.add(key_component_1)
    
    while queue:
        current = queue.popleft()
        if current == key_component_2:
            return 'Yes'
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return 'No'
