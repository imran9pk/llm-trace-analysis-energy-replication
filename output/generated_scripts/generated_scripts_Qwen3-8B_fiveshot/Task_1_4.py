"""
Auto-generated task-level solver.

Task ID: Task_1_4
Task Type: 1_Entity
Task Description: Identify which service instances call a given service instance.
Question Template: Which service instances call the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    service_instances = []
    for span in trace1:
        if span['service.name'] == key_component:
            if span['parentSpanId'] != '-1':
                service_instances.append(span['parentSpanId'])
    return service_instances
