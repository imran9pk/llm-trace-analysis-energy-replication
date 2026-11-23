"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    callee_services = []
    for span in trace1:
        if span['service.name'] == key_component:
            for parent_span in trace1:
                if parent_span['spanId'] == span['parentSpanId']:
                    callee_services.append(parent_span['service.name'])
    return list(set(callee_services))
