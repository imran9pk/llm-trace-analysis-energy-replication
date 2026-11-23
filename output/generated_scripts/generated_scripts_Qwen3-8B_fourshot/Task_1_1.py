"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    services_called = set()
    spans = trace1
    service_to_spans = {}
    
    for span in spans:
        if span['service.name'] not in service_to_spans:
            service_to_spans[span['service.name']] = []
        service_to_spans[span['service.name']].append(span)
    
    for span in spans:
        if span['service.name'] == key_component:
            if span['parentSpanId'] != '-1':
                parent_span = next((s for s in spans if s['spanId'] == span['parentSpanId']), None)
                if parent_span:
                    if parent_span['service.name'] not in services_called:
                        services_called.add(parent_span['service.name'])
    
    return list(services_called)
