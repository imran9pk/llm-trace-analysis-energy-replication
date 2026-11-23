"""
Auto-generated task-level solver.

Task ID: Task_3_20
Task Type: 6_Entity
Task Description: Identify the operations with abnormal response codes in a given trace.
Question Template: Which operations have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    def is_abnormal(response_code):
        return response_code != 'OK' and response_code != '200'

    abnormal_spans = []
    for span in trace1:
        if is_abnormal(span['status']['code']):
            abnormal_spans.append(span['name'])
    return abnormal_spans
