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
            graph[span['spanId']].append(span['parentSpanId'])
        elif span['service.name'] == key_component_2:
            graph[span['spanId']].append(-1)
        else:
            if span['parentSpanId'] != -1:
                graph[span['parentSpanId']].append(span['spanId'])

    visited = set()
    queue = deque([(-1, False)]
    while queue:
        parent, is_key_component_2 = queue.popleft()
        if parent != -1 and parent not in visited:
            visited.add(parent)
            if is_key_component_2:
                return 'Yes'
            for child in graph[parent]:
                if child not in visited:
                    queue.append((child, False))
        if parent == -1:
            queue.append((-1, True))

    return 'No'
