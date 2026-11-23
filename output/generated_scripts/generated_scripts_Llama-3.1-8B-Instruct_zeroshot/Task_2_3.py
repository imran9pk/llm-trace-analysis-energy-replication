"""
Auto-generated task-level solver.

Task ID: Task_2_3
Task Type: 3_Existence
Task Description: Determine whether a service call path from a source service to a destination service exists in a given trace.
Question Template: Is there an HTTP call path from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    graph = {}
    for span in trace1:
        if span['service.name'] not in graph:
            graph[span['service.name']] = []
        if span['parentSpanId'] != -1:
            if span['parentSpanId'] not in graph:
                graph[span['parentSpanId']] = []
            graph[span['parentSpanId']].append(span['service.name'])
    
    def dfs(node, target, visited):
        if node == target:
            return True
        if node in visited:
            return False
        visited.add(node)
        if node in graph:
            for neighbor in graph[node]:
                if dfs(neighbor, target, visited):
                    return True
        return False
    
    return 'Yes' if dfs(key_component_1, key_component_2, set()) else 'No'
