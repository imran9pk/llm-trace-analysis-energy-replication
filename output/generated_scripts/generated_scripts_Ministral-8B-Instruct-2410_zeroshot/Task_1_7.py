"""
Auto-generated task-level solver.

Task ID: Task_1_7
Task Type: 2_Computation
Task Description: Identify the response time of a given span.
Question Template: What is the response time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    for span in trace1:
        if span['name'] == key_component:
            start_time = int(span['startTimeUnixNano'])
            end_time = int(span['endTimeUnixNano'])
            return end_time - start_time
    return 0
