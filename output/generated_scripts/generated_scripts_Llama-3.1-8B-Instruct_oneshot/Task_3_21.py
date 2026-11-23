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
        if int(span['http.status_code']) != 200:
            abnormal_spans.append(span)
    return abnormal_spans
