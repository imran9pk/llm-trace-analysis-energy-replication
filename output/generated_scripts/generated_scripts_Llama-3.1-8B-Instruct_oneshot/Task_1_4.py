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
        if span['service.name'] not in graph:
            graph[span['service.name']] = []
        if span['parentSpanId'] != '-1':
            if span['parentSpanId'] not in graph:
                graph[span['parentSpanId']] = []
            graph[span['parentSpanId']].append(span['service.name'])
        else:
            graph[span['service.name']].append(None)
    
    def dfs(node, visited, path):
        if node not in graph:
            return []
        visited.add(node)
        paths = []
        for neighbor in graph[node]:
            if neighbor not in visited:
                paths.extend(dfs(neighbor, visited, path + [node]))
        paths.append(path + [node])
        return paths
    
    visited = set()
    paths = dfs(key_component, visited, [])
    return [path[-2] for path in paths if path[-1] == key_component]
