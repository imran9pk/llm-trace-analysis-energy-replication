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
            if span['parentSpanId'] == parent_span_id and span['service.name'] == service_name:
                return span
        return None

    def find_caller(trace, service_name):
        for span in trace:
            if span['service.name'] == service_name:
                return dfs(trace, span['spanId'], service_name)
        return None

    def find_callee(trace, service_name):
        for span in trace:
            if span['service.name'] == service_name:
                return span
        return None

    caller = find_caller(trace1, key_component_1)
    callee = find_callee(trace1, key_component_2)

    if caller is None or callee is None:
        return 'No'

    for span in trace1:
        if span['service.name'] == key_component_1 and span['parentSpanId'] == callee['spanId']:
            return 'Yes'

    return 'No'
