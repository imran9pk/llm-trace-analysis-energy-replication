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
    service_name_to_spans = {}
    
    for span in spans:
        service_name = span['service.name']
        if service_name not in service_name_to_spans:
            service_name_to_spans[service_name] = []
        service_name_to_spans[service_name].append(span)
    
    for service, spans_list in service_name_to_spans.items():
        if service == key_component:
            for span in spans_list:
                if span['parentSpanId'] != '-1':
                    parent_service = None
                    for parent_span in spans_list:
                        if parent_span['spanId'] == span['parentSpanId']:
                            parent_service = parent_span['service.name']
                            break
                    if parent_service:
                        services_called.add(parent_service)
    
    return list(services_called)
