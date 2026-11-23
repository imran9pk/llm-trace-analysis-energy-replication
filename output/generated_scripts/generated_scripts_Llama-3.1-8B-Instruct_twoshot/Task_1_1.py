"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_callees(trace, service):
        callees = set()
        for span in trace:
            if span['service.name'] == service and span['parentSpanId'] != '-1':
                callees.add(span['parentSpanId'])
        return callees

    callees = get_callees(trace1, key_component)
    called_services = set()
    for span in trace1:
        if span['spanId'] in callees:
            called_services.add(span['service.name'])
    return list(called_services)
