"""
Auto-generated task-level solver.

Task ID: Task_2_3
Task Type: 3_Existence
Task Description: Determine whether a service call path from a source service to a destination service exists in a given trace.
Question Template: Is there an HTTP call path from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def dfs(trace, target_service, visited):
        for span in trace:
            if span['service.name'] == target_service and span['spanId'] not in visited:
                visited.add(span['spanId'])
                if span['parentSpanId'] == '-1' or dfs(trace, span['service.name'], visited):
                    return True
        return False

    for span in trace1:
        if span['service.name'] == key_component_1:
            return 'Yes' if dfs(trace1, key_component_2, set()) else 'No'
    return 'No'
