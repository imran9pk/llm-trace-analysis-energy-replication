"""
Auto-generated task-level solver.

Task ID: Task_1_4
Task Type: 1_Entity
Task Description: Identify which service instances call a given service instance.
Question Template: Which service instances call the service instance '{key_component}' in the Input Trace?
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
    
    def dfs(node, visited, path, target):
        if node == target:
            return path + [node]
        if node in visited:
            return []
        visited.add(node)
        for neighbor in graph.get(node, []):
            result = dfs(neighbor, visited, path + [node], target)
            if result:
                return result
        return []
    
    visited = set()
    for node in graph:
        result = dfs(node, visited, [], key_component)
        if result:
            return result
    return []
