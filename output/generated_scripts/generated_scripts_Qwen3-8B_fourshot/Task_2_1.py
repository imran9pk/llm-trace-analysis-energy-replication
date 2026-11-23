"""
Auto-generated task-level solver.

Task ID: Task_2_1
Task Type: 3_Existence
Task Description: Determine whether a specified service call pair exists in a given trace.
Question Template: Is there an HTTP call from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    for span in trace1:
        if span['kind'] == 'SPAN_KIND_CLIENT':
            if span['service.name'] == key_component_1:
                if span['http.route'] and span['http.route'].startswith('GET') or span['http.route'].startswith('POST') or span['http.route'].startswith('PUT') or span['http.route'].startswith('DELETE'):
                    if span['service.name'] == key_component_2:
                        return 'Yes'
    return 'No'
