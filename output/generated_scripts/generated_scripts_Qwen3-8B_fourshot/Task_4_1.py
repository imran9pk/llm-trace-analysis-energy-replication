"""
Auto-generated task-level solver.

Task ID: Task_4_1
Task Type: 7_Comparison
Task Description: Determine whether the response codes of two given traces are the same.
Question Template: Are the response codes of the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_root_span(trace):
        for span in trace:
            if span['parentSpanId'] == '-1':
                return span
        return None

    root_span1 = get_root_span(trace1)
    root_span2 = get_root_span(trace2)

    if not root_span1 or not root_span2:
        return 'No'

    http_status_code1 = root_span1.get('http.status_code')
    http_status_code2 = root_span2.get('http.status_code')

    if http_status_code1 == http_status_code2:
        return 'Yes'
    else:
        return 'No'
