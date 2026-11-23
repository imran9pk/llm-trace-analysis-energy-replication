"""
Auto-generated task-level solver.

Task ID: Task_4_7
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instances.
Question Template: Are the sets of service instances involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_service_instances(trace):
        service_instances = set()
        for span in trace:
            service_instances.add(span['service.name'])
        return service_instances

    trace1_instances = get_service_instances(trace1)
    trace2_instances = get_service_instances(trace2)

    return 'Yes' if trace1_instances == trace2_instances else 'No'
