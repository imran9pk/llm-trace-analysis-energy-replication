"""
Auto-generated task-level solver.

Task ID: Task_4_1
Task Type: 7_Comparison
Task Description: Determine whether the response codes of two given traces are the same.
Question Template: Are the response codes of the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_response_code(trace):
        for span in trace:
            if span.get('name') == 'HTTP Response':
                return span.get('attributes', {}).get('http.status_code')
        return None

    code1 = get_response_code(trace1)
    code2 = get_response_code(trace2)
    return 'Yes' if code1 == code2 else 'No'
