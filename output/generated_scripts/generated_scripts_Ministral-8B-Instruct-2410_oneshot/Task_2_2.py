"""
Auto-generated task-level solver.

Task ID: Task_2_2
Task Type: 3_Existence
Task Description: Determine whether a specified service instance call pair exists in a given trace.
Question Template: Is there an HTTP call from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    for span in trace1:
        if span['service.name'] == key_component_1 and span['http.route']:
            for child_span in trace1:
                if child_span['parentSpanId'] == span['spanId'] and child_span['service.name'] == key_component_2 and child_span['http.route']:
                    return 'Yes'
    return 'No'
