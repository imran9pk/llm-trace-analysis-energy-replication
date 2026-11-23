"""
Auto-generated task-level solver.

Task ID: Task_4_8
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of operations.
Question Template: Are the sets of operations involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    # Convert the traces to sets of operations
    trace1_set = set((span['name'], span['kind']) for span in trace1)
    trace2_set = set((span['name'], span['kind']) for span in trace2)

    # Compare the sets of operations
    return 'Yes' if trace1_set == trace2_set else 'No'
