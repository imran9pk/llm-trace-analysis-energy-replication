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
    service_instances = set()
    
    for span in trace1:
        service_name = span['service.name']
        host_name = span['host.name']
        service_instance = f"{service_name}-{host_name}"
        service_instances.add(service_instance)
        
        if span['parentSpanId'] != '-1':
            parent_service_instance = f"{span['service.name']}-{span['host.name']}"
            graph[parent_service_instance].append(service_instance)
    
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
        for neighbor in graph[current]:
            queue.append(neighbor)
    
    return 'No'
