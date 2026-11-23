"""
Auto-generated task-level solver.

Task ID: Task_2_1
Task Type: 3_Existence
Task Description: Determine whether a specified service call pair exists in a given trace.
Question Template: Is there an HTTP call from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    caller_service = key_component_1
    callee_service = key_component_2
    for span in trace1:
        if span['kind'] == 'SPAN_KIND_CLIENT' and span['service.name'] == caller_service:
            parent_span = next((s for s in trace1 if s['spanId'] == span['parentSpanId']), None)
            if parent_span and parent_span['service.name'] == callee_service:
                return 'Yes'
    return 'No'
