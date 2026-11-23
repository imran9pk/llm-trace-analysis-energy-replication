"""
Auto-generated task-level solver.

Task ID: Task_2_4
Task Type: 3_Existence
Task Description: Determine whether a service instance call path from a source service instance to a destination service instance exists in a given trace.
Question Template: Is there an HTTP call path from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def dfs(span, target):
        if span['service.name'] == target:
            return True
        if span['parentSpanId'] == -1:
            return False
        for child in [s for s in trace1 if s['parentSpanId'] == span['spanId']]:
            if dfs(child, target):
                return True
        return False

    for span in trace1:
        if span['service.name'] == key_component_1:
            return 'Yes' if dfs(span, key_component_2) else 'No'
    return 'No'
