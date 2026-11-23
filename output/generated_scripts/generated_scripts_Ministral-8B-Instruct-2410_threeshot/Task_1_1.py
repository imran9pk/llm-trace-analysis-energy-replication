"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    called_services = []
    for span in trace1:
        if span['parentSpanId'] == -1:
            continue
        if span['service.name'] == key_component:
            called_services.append(span['service.name'])
    return called_services
