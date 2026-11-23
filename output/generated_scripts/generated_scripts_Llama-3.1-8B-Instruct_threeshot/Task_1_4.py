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
        graph[span['spanId']] = span['service.name']
        if 'parentSpanId' in span and span['parentSpanId'] != '-1':
            if span['parentSpanId'] not in graph:
                graph[span['parentSpanId']] = None
            if span['service.name'] not in graph:
                graph[span['service.name']] = {}
            if span['parentSpanId'] not in graph[span['service.name']]:
                graph[span['service.name']][span['parentSpanId']] = []
            graph[span['service.name']][span['parentSpanId']].append(span['spanId'])

    def dfs(service_name, target_service_name, visited=None):
        if visited is None:
            visited = set()
        visited.add(service_name)
        if service_name == target_service_name:
            return [service_name]
        if service_name not in graph:
            return []
        if target_service_name in graph[service_name]:
            return [target_service_name]
        result = []
        for parent in graph[service_name]:
            if parent not in visited:
                result.extend(dfs(graph[parent], target_service_name, visited))
        return result

    return dfs(key_component, key_component)
