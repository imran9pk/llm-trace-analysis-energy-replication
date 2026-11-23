"""
Auto-generated task-level solver.

Task ID: Task_2_4
Task Type: 3_Existence
Task Description: Determine whether a service instance call path from a source service instance to a destination service instance exists in a given trace.
Question Template: Is there an HTTP call path from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    for span in trace1:
        if span['service.name'] == key_component_1 and span['host.name'] == key_component_1:
            for child_span in trace1:
                if child_span['parentSpanId'] == span['spanId']:
                    if child_span['service.name'] == key_component_2 and child_span['host.name'] == key_component_2:
                        return 'Yes'
    return 'No'
