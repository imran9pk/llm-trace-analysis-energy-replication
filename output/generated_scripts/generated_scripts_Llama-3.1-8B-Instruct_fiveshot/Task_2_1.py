"""
Auto-generated task-level solver.

Task ID: Task_2_1
Task Type: 3_Existence
Task Description: Determine whether a specified service call pair exists in a given trace.
Question Template: Is there an HTTP call from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def dfs(trace, parent_span_id, service_name):
        for span in trace:
            if span['service.name'] == service_name and span['parentSpanId'] == parent_span_id:
                return True
            if span['service.name'] == service_name:
                return False
            if span['parentSpanId'] != '-1':
                if dfs(trace, span['spanId'], service_name):
                    return True
        return False

    for span in trace1:
        if span['service.name'] == key_component_1 and dfs(trace1, span['spanId'], key_component_2):
            return 'Yes'
    return 'No'
