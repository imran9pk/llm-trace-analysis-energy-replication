"""
Auto-generated task-level solver.

Task ID: Task_2_2
Task Type: 3_Existence
Task Description: Determine whether a specified service instance call pair exists in a given trace.
Question Template: Is there an HTTP call from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
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
        if span['service.name'] == key_component_1 and dfs(span, key_component_2):
            return 'Yes'
    return 'No'
