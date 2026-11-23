"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    # Build a map from host.name to service instances
    service_instances = {}
    for span in trace1:
        host_name = span['host.name']
        if host_name not in service_instances:
            service_instances[host_name] = []
        service_instances[host_name].append(span['service.name'])
    
    # Find all spans that have the key_component as their host.name
    caller_spans = [span for span in trace1 if span['host.name'] == key_component]
    
    # Collect all service instances called by these spans
    called_services = set()
    for span in caller_spans:
        if span['parentSpanId'] != '-1':
            parent_span = next((s for s in trace1 if s['spanId'] == span['parentSpanId']), None)
            if parent_span:
                called_services.add(parent_span['service.name'])
    
    return list(called_services)
