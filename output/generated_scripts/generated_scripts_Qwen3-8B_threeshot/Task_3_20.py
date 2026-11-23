"""
Auto-generated task-level solver.

Task ID: Task_3_20
Task Type: 6_Entity
Task Description: Identify the operations with abnormal response codes in a given trace.
Question Template: Which operations have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    abnormal_codes = [span['name'] for span in trace1 if 'http.status_code' in span and int(span['http.status_code']) not in [200, 201, 202, 204, 301, 302, 303, 307, 308]]
    return abnormal_codes
