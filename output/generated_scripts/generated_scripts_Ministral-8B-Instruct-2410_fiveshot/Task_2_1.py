"""
Auto-generated task-level solver.

Task ID: Task_2_1
Task Type: 3_Existence
Task Description: Determine whether a specified service call pair exists in a given trace.
Question Template: Is there an HTTP call from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    for span in trace1:
        if span['service.name'] == key_component_1 and span['http.route'] and key_component_2 in span['http.route']:
            return 'Yes'
    return 'No'
