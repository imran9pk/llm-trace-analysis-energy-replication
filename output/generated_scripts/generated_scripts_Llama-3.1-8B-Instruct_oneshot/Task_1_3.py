"""
Auto-generated task-level solver.

Task ID: Task_1_3
Task Type: 1_Entity
Task Description: Identify which services call a given service.
Question Template: Which services call the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    graph = {}
    for span in trace1:
        if span['parentSpanId'] not in graph:
            graph[span['parentSpanId']] = []
        graph[span['parentSpanId']].append(span['spanId'])
        if span['spanId'] not in graph:
            graph[span['spanId']] = []
    
    def dfs(node):
        if node in graph:
            return graph[node]
        else:
            return []
    
    def get_callers(key_component):
        callers = []
        for span in trace1:
            if span['service.name'] == key_component and span['parentSpanId'] != -1:
                callers.extend(dfs(span['parentSpanId']))
        return list(set(callers))
    
    return get_callers(key_component)
