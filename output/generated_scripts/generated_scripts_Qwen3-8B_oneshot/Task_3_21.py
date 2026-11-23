"""
Auto-generated task-level solver.

Task ID: Task_3_21
Task Type: 6_Entity
Task Description: Identify the spans with abnormal response codes in a given trace.
Question Template: Which spans have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    abnormal_spans = []
    for span in trace1:
        if 'http.status_code' in span:
            status_code = int(span['http.status_code'])
            if status_code >= 400:
                abnormal_spans.append(span['spanId'])
    return abnormal_spans
