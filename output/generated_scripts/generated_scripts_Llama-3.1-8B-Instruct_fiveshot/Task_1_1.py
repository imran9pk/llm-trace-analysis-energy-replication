"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    graph = {}
    for span in trace1:
        if span['parentSpanId'] not in graph:
            graph[span['parentSpanId']] = []
        graph[span['parentSpanId']].append(span['service.name'])
        if span['spanId'] not in graph:
            graph[span['spanId']] = []
        graph[span['spanId']].append(span['service.name'])
    
    def dfs(node, visited, path):
        if node in visited:
            return []
        visited.add(node)
        path.append(node)
        if node not in graph:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                path = dfs(neighbor, visited, path)
        return path
    
    visited = set()
    return dfs(key_component, visited, [])
