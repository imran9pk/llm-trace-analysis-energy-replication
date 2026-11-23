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
    graph = defaultdict(set)
    service_to_spans = defaultdict(list)
    
    for span in trace1:
        service_name = span['service.name']
        service_to_spans[service_name].append(span)
    
    # Build the call graph
    for span in trace1:
        if span['parentSpanId'] != '-1':
            parent_service = None
            for s in trace1:
                if s['spanId'] == span['parentSpanId']:
                    parent_service = s['service.name']
                    break
            if parent_service:
                graph[parent_service].add(span['service.name'])
    
    # Check for path using BFS
    visited = set()
    queue = deque([key_component_1])
    visited.add(key_component_1)
    
    while queue:
        current = queue.popleft()
        if current == key_component_2:
            return 'Yes'
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return 'No'
