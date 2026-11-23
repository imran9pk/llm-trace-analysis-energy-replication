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
            if span['parentSpanId'] == -1:
                return span
        return None

    def get_response_code(span):
        return span['status']['code']

    root1 = get_root_span(trace1)
    root2 = get_root_span(trace2)

    if root1 is None or root2 is None:
        return 'No'

    return 'Yes' if get_response_code(root1) == get_response_code(root2) else 'No'
