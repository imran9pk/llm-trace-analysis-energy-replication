"""
Auto-generated task-level solver.

Task ID: Task_2_2
Task Type: 3_Existence
Task Description: Determine whether a specified service instance call pair exists in a given trace.
Question Template: Is there an HTTP call from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    caller_found = False
    callee_found = False
    for span in trace1:
        if span['service.name'] == key_component_1:
            caller_found = True
        if span['service.name'] == key_component_2:
            callee_found = True
        if caller_found and callee_found:
            return 'Yes'
    return 'No'
