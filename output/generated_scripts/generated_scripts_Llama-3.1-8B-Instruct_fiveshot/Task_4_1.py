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
        return http_status_codes[0] if http_status_codes else None

    def get_http_status_codes(trace):
        http_status_codes = [span.get('http.status_code') for span in trace if 'http.status_code' in span]
        return http_status_codes

    trace1_http_status_code = get_http_status_code(trace1)
    trace2_http_status_code = get_http_status_code(trace2)

    if trace1_http_status_code is None or trace2_http_status_code is None:
        return []

    trace1_http_status_codes = get_http_status_codes(trace1)
    trace2_http_status_codes = get_http_status_codes(trace2)

    if len(trace1_http_status_codes) != len(trace2_http_status_codes):
        return []

    for code1, code2 in zip(trace1_http_status_codes, trace2_http_status_codes):
        if code1 != code2:
            return []

    return ['Yes']
