"""
Auto-generated task-level solver.

Task ID: Task_4_6
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of services.
Question Template: Are the sets of services involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_service_names(trace):
        return {span['service.name'] for span in trace}

    return 'Yes' if get_service_names(trace1) == get_service_names(trace2) else 'No'
