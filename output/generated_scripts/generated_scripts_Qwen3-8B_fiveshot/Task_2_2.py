"""
Auto-generated task-level solver.

Task ID: Task_2_2
Task Type: 3_Existence
Task Description: Determine whether a specified service instance call pair exists in a given trace.
Question Template: Is there an HTTP call from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    caller_service = None
    callee_service = None
    for span in trace1:
        if span['service.name'] == key_component_1 and span['host.name'] == key_component_1:
            caller_service = span
        if span['service.name'] == key_component_2 and span['host.name'] == key_component_2:
            callee_service = span
    if caller_service is None or callee_service is None:
        return "No"
    for span in trace1:
        if span['parentSpanId'] == caller_service['spanId']:
            if span['service.name'] == key_component_2 and span['host.name'] == key_component_2:
                return "Yes"
    return "No"
