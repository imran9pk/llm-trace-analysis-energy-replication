"""
Auto-generated task-level solver.

Task ID: Task_2_2
Task Type: 3_Existence
Task Description: Determine whether a specified service instance call pair exists in a given trace.
Question Template: Is there an HTTP call from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def dfs(trace, parent_span_id, caller_service, callee_service):
        for span in trace:
            if span['parentSpanId'] == parent_span_id:
                if span['service.name'] == callee_service:
                    return True
                if span['service.name'] == caller_service:
                    return dfs(trace, span['spanId'], caller_service, callee_service)
        return False

    for span in trace1:
        if span['service.name'] == key_component_1 and dfs(trace1, span['spanId'], key_component_1, key_component_2):
            return 'Yes'
    return 'No'
