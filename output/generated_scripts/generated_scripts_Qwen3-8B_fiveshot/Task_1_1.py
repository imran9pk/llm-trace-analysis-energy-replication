"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    called_services = set()
    spans = trace1
    # Build a map from service name to list of spans
    service_to_spans = {}
    for span in spans:
        service_name = span['service.name']
        if service_name not in service_to_spans:
            service_to_spans[service_name] = []
        service_to_spans[service_name].append(span)
    
    # Find all spans that belong to the key_component
    key_spans = service_to_spans.get(key_component, [])
    
    # For each key span, check its children (spans with parentSpanId equal to this span's spanId)
    # and collect the service names of those children
    for key_span in key_spans:
        key_span_id = key_span['spanId']
        for span in spans:
            if span['parentSpanId'] == key_span_id:
                called_services.add(span['service.name'])
    
    return list(called_services)
