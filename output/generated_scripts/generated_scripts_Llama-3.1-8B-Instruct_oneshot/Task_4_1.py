"""
Auto-generated task-level solver.

Task ID: Task_4_1
Task Type: 7_Comparison
Task Description: Determine whether the response codes of two given traces are the same.
Question Template: Are the response codes of the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_response_codes(trace):
        response_codes = set()
        for span in trace:
            if 'http.status_code' in span:
                response_codes.add(span['http.status_code'])
        return response_codes

    trace1_codes = get_response_codes(trace1)
    trace2_codes = get_response_codes(trace2)
    return 'Yes' if trace1_codes == trace2_codes else 'No'
