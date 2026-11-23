"""
Auto-generated task-level solver.

Task ID: Task_4_6
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of services.
Question Template: Are the sets of services involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_services(trace):
        services = set()
        for span in trace:
            services.add(span['service.name'])
        return services

    trace1_services = get_services(trace1)
    trace2_services = get_services(trace2)

    return 'Yes' if trace1_services == trace2_services else 'No'
