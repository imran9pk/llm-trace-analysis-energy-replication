"""
Auto-generated task-level solver.

Task ID: Task_2_2
Task Type: 3_Existence
Task Description: Determine whether a specified service instance call pair exists in a given trace.
Question Template: Is there an HTTP call from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def dfs(trace, key_component_1, key_component_2, visited=None):
        if visited is None:
            visited = set()
        for span in trace:
            if span['service.name'] == key_component_1 and span['host.name'] == key_component_2:
                return True
            if span['service.name'] == key_component_2 and span['host.name'] == key_component_1:
                return True
            if span['spanId'] not in visited:
                visited.add(span['spanId'])
                if span['parentSpanId'] != -1:
                    if dfs(trace, key_component_1, key_component_2, visited):
                        return True
        return False

    return 'Yes' if dfs(trace1, key_component_1, key_component_2) else 'No'
