"""
Auto-generated task-level solver.

Task ID: Task_2_4
Task Type: 3_Existence
Task Description: Determine whether a service instance call path from a source service instance to a destination service instance exists in a given trace.
Question Template: Is there an HTTP call path from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    from collections import defaultdict, deque

    # Build a graph of spans
    graph = defaultdict(list)
    span_map = {}
    for span in trace1:
        span_id = span['spanId']
        parent_id = span['parentSpanId']
        service_name = span['service.name']
        span_map[span_id] = service_name
        if parent_id != -1:
            graph[parent_id].append(span_id)

    # BFS to find path from source to destination
    visited = set()
    queue = deque([(key_component_1, None)])
    while queue:
        current, parent = queue.popleft()
        if current == key_component_2:
            return "Yes"
        if current in visited:
            continue
        visited.add(current)
        for child in graph.get(current, []):
            queue.append((span_map[child], current))
    return "No"
