"""
Auto-generated task-level solver.

Task ID: Task_4_2
Task Type: 7_Comparison
Task Description: Determine whether the root URLs of two given traces are the same.
Question Template: Are the root URLs of the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_root_url(trace):
        for span in trace:
            if span['parentSpanId'] == -1:
                return span['http.route']
        return None

    root_url1 = get_root_url(trace1)
    root_url2 = get_root_url(trace2)

    return 'Yes' if root_url1 == root_url2 else 'No'
