"""
Auto-generated task-level solver.

Task ID: Task_3_20
Task Type: 6_Entity
Task Description: Identify the operations with abnormal response codes in a given trace.
Question Template: Which operations have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    abnormal_codes = [span['http.status_code'] for span in trace1 if span['http.status_code'] not in ['200', '201', '202', '204', '301', '302', '303', '304', '307', '308', '400', '401', '403', '404', '405', '406', '407', '408', '409', '410', '411', '412', '413', '414', '415', '416', '417', '418', '421', '422', '423', '424', '425', '426', '428', '429', '431', '451', '500', '501', '502', '503', '504', '505', '506', '507', '508', '510', '511']]
    return abnormal_codes
