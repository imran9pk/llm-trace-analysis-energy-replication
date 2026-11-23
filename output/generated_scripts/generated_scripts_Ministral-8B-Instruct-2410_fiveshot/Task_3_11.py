"""
Auto-generated task-level solver.

Task ID: Task_3_11
Task Type: 6_Computation
Task Description: Identify the end-to-end response time of a given trace.
Question Template: What is the end-to-end response time of the Input Trace?
"""

def solution(trace1):
    root_span = next(span for span in trace1 if span['parentSpanId'] == '-1')
    return int(root_span['durationTimeUnixNano'])
