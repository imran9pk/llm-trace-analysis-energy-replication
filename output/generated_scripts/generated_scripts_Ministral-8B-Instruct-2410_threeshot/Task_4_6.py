"""
Auto-generated task-level solver.

Task ID: Task_4_6
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of services.
Question Template: Are the sets of services involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    # Extract the set of services involved in each trace
    services_trace1 = set(span['service.name'] for span in trace1)
    services_trace2 = set(span['service.name'] for span in trace2)

    # Compare the sets of services
    return 'Yes' if services_trace1 == services_trace2 else 'No'
