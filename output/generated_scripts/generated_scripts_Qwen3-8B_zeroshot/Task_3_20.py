"""
Auto-generated task-level solver.

Task ID: Task_3_20
Task Type: 6_Entity
Task Description: Identify the operations with abnormal response codes in a given trace.
Question Template: Which operations have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    abnormal_ops = []
    for span in trace1:
        if 'http.status_code' in span.get('attributes', {}):
            status_code = int(span['attributes']['http.status_code'])
            if status_code >= 400:
                abnormal_ops.append(span['spanId'])
    return abnormal_ops
