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
    seen_parent_ids = set()
    for span in trace1:
        if span['parentSpanId'] != -1 and span['service.name'] == callee_service:
            seen_parent_ids.add(span['parentSpanId'])
    for span in trace1:
        if span['spanId'] in seen_parent_ids and span['service.name'] == caller_service:
            return "Yes"
    return "No"
