"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    graph = {}
    for span in trace1:
        graph[span['spanId']] = span['service.name']
        if 'parentSpanId' in span and span['parentSpanId'] != '-1':
            if span['parentSpanId'] not in graph:
                graph[span['parentSpanId']] = None
            if span['service.name'] not in graph:
                graph[span['service.name']] = {}
            if span['parentSpanId'] not in graph[span['service.name']]:
                graph[span['service.name']][span['parentSpanId']] = []
            graph[span['service.name']][span['parentSpanId']].append(span['spanId'])

    def dfs(service_name, visited, path):
        if service_name not in graph:
            return []
        if service_name in visited:
            return []
        visited.add(service_name)
        path.append(service_name)
        if service_name not in graph:
            return path
        for parent in graph[service_name]:
            if parent is not None:
                path.extend(dfs(graph[parent], visited, path))
        return path

    visited = set()
    result = dfs(key_component, visited, [])
    return [service for service in result if service != key_component]
