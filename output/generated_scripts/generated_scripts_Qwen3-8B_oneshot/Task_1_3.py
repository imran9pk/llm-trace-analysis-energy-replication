"""
Auto-generated task-level solver.

Task ID: Task_1_3
Task Type: 1_Entity
Task Description: Identify which services call a given service.
Question Template: Which services call the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    callers = []
    service_names = set()
    for span in trace1:
        if span['service.name'] == key_component:
            service_names.add(span['service.name'])
    for span in trace1:
        if span['service.name'] in service_names:
            if span['parentSpanId'] != '-1':
                parent_service = next((s['service.name'] for s in trace1 if s['spanId'] == span['parentSpanId']), None)
                if parent_service:
                    callers.append(parent_service)
    return list(set(callers))
