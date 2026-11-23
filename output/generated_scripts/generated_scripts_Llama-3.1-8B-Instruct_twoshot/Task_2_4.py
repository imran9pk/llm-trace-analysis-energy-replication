"""
Auto-generated task-level solver.

Task ID: Task_2_4
Task Type: 3_Existence
Task Description: Determine whether a service instance call path from a source service instance to a destination service instance exists in a given trace.
Question Template: Is there an HTTP call path from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    graph = {}
    for span in trace1:
        if span['service.name'] not in graph:
            graph[span['service.name']] = {}
        if span['host.name'] not in graph[span['service.name']]:
            graph[span['service.name']][span['host.name']] = []
        if span['parentSpanId'] != -1:
            graph[span['service.name']][span['host.name']].append((span['parentSpanId'], span['service.name'], span['host.name']))
    
    def dfs(current_service, current_host, target_service, target_host, visited):
        if current_service == target_service and current_host == target_host:
            return True
        if (current_service, current_host) in visited:
            return False
        visited.add((current_service, current_host))
        if current_service not in graph:
            return False
        if current_host not in graph[current_service]:
            return False
        for parent_span_id, parent_service, parent_host in graph[current_service][current_host]:
            if dfs(parent_service, parent_host, target_service, target_host, visited):
                return True
        return False
    
    return 'Yes' if dfs(key_component_1, None, key_component_2, None, set()) else 'No'
