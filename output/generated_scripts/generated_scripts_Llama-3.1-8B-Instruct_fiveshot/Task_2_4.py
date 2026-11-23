"""
Auto-generated task-level solver.

Task ID: Task_2_4
Task Type: 3_Existence
Task Description: Determine whether a service instance call path from a source service instance to a destination service instance exists in a given trace.
Question Template: Is there an HTTP call path from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

from collections import defaultdict, deque

def solution(trace1, key_component_1, key_component_2):
    graph = defaultdict(list)
    for span in trace1:
        if span['service.name'] == key_component_1:
            graph[span['host.name']].append(span['spanId'])
        elif span['service.name'] == key_component_2:
            graph[span['host.name']].append(span['spanId'])
        for neighbor in trace1:
            if neighbor['spanId'] == span['spanId']:
                if neighbor['parentSpanId'] != -1:
                    graph[neighbor['host.name']].append(neighbor['parentSpanId'])
                break

    visited = set()
    queue = deque([graph[key_component_1]])
    while queue:
        current = queue.popleft()
        for neighbor in graph:
            if neighbor not in visited and current & graph[neighbor]:
                visited.add(neighbor)
                queue.append(graph[neighbor])
    return 'Yes' if key_component_2 in visited else 'No'
