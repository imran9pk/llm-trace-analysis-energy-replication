"""
Auto-generated task-level solver.

Task ID: Task_4_7
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instances.
Question Template: Are the sets of service instances involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    # Extract the service names from the traces
    service_names1 = {span['service.name'] for span in trace1}
    service_names2 = {span['service.name'] for span in trace2}

    # Compare the sets of service names
    return 'Yes' if service_names1 == service_names2 else 'No'
