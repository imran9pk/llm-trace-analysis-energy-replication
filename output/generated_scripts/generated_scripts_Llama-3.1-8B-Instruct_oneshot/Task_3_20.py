"""
Auto-generated task-level solver.

Task ID: Task_3_20
Task Type: 6_Entity
Task Description: Identify the operations with abnormal response codes in a given trace.
Question Template: Which operations have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    def is_abnormal(status_code):
        return int(status_code) != 200

    abnormal_spans = [span for span in trace1 if is_abnormal(span['http.status_code'])]
    return abnormal_spans
