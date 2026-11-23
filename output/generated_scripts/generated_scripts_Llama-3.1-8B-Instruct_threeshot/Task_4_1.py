"""
Auto-generated task-level solver.

Task ID: Task_4_1
Task Type: 7_Comparison
Task Description: Determine whether the response codes of two given traces are the same.
Question Template: Are the response codes of the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_http_status_code(trace):
        http_status_codes = [span.get('http.status_code') for span in trace if 'http.status_code' in span]
        return http_status_codes

    def are_http_status_codes_equal(trace1, trace2):
        http_status_codes1 = get_http_status_codes(trace1)
        http_status_codes2 = get_http_status_codes(trace2)
        return set(http_status_codes1) == set(http_status_codes2)

    return 'Yes' if are_http_status_codes_equal(trace1, trace2) else 'No'
