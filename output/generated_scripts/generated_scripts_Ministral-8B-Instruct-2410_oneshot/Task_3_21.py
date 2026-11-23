"""
Auto-generated task-level solver.

Task ID: Task_3_21
Task Type: 6_Entity
Task Description: Identify the spans with abnormal response codes in a given trace.
Question Template: Which spans have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    abnormal_codes = [span for span in trace1 if span.get('http.status_code') and int(span['http.status_code']) >= 400]
    return abnormal_codes
