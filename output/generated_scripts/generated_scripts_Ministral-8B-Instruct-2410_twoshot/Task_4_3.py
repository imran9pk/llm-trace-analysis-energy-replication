"""
Auto-generated task-level solver.

Task ID: Task_4_3
Task Type: 8_Comparison
Task Description: Identify the trace with a greater number of spans between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater number of spans?
"""

def solution(trace1, trace2):
    return 'Same' if len(trace1) == len(trace2) else 'Input Trace ' + ('1' if len(trace1) > len(trace2) else '2')
