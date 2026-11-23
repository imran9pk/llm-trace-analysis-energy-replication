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

    def get_trace_id(trace):
        return trace[0].get('traceId')

    trace1_id = get_trace_id(trace1)
    trace2_id = get_trace_id(trace2)

    if trace1_id != trace2_id:
        return []

    http_status_code1 = get_http_status_code(trace1)
    http_status_code2 = get_http_status_code(trace2)

    if http_status_code1 != http_status_code2:
        return []

    return ['Yes']
