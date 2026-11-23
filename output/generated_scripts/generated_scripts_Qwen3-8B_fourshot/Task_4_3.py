"""
Auto-generated task-level solver.

Task ID: Task_4_3
Task Type: 8_Comparison
Task Description: Identify the trace with a greater number of spans between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater number of spans?
"""

def solution(trace1, trace2):
    def count_spans(trace):
        return len(trace)
    count1 = count_spans(trace1)
    count2 = count_spans(trace2)
    if count1 > count2:
        return trace1[0]['traceId']
    elif count2 > count1:
        return trace2[0]['traceId']
    else:
        return 'Same'
