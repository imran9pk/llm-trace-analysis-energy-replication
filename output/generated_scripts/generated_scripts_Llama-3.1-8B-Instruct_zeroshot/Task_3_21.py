"""
Auto-generated task-level solver.

Task ID: Task_3_21
Task Type: 6_Entity
Task Description: Identify the spans with abnormal response codes in a given trace.
Question Template: Which spans have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    def is_abnormal(code):
        return code >= 400 and code < 600

    abnormal_spans = []
    for span in trace1:
        if is_abnormal(int(span['status']['code'])):
            abnormal_spans.append(span['spanId'])

    return abnormal_spans
