"""
Auto-generated task-level solver.

Task ID: Task_4_3
Task Type: 8_Comparison
Task Description: Identify the trace with a greater number of spans between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater number of spans?
"""

def solution(trace1, trace2):
    span_count1 = len(trace1)
    span_count2 = len(trace2)
    if span_count1 > span_count2:
        return 1
    elif span_count2 > span_count1:
        return 2
    else:
        return "Same"
