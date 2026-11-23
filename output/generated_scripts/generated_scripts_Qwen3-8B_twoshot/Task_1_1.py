"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    called_services = set()
    service_to_spans = {}
    
    for span in trace1:
        service_name = span['service.name']
        if service_name not in service_to_spans:
            service_to_spans[service_name] = []
        service_to_spans[service_name].append(span)
    
    for service, spans in service_to_spans.items():
        if service == key_component:
            for span in spans:
                if span['parentSpanId'] != '-1':
                    parent_service = None
                    for parent_span in service_to_spans.values():
                        for ps in parent_span:
                            if ps['spanId'] == span['parentSpanId']:
                                parent_service = ps['service.name']
                                break
                        if parent_service:
                            break
                    if parent_service:
                        called_services.add(parent_service)
    
    return list(called_services)
