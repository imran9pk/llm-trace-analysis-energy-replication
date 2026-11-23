"""
Auto-generated task-level solver.

Task ID: Task_3_20
Task Type: 6_Entity
Task Description: Identify the operations with abnormal response codes in a given trace.
Question Template: Which operations have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    abnormal_codes = []
    for span in trace1:
        if 'http.status_code' in span:
            status_code = int(span['http.status_code'])
            if status_code >= 400:
                abnormal_codes.append(span['name'])
    return abnormal_codes
