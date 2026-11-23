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
    called_services = []
    for span in trace1:
        if span['host.name'] == key_component:
            # Check if this span is a client span (caller)
            if span['kind'] == 'SPAN_KIND_CLIENT':
                # Find all child spans (callee)
                for child in trace1:
                    if child['parentSpanId'] == span['spanId']:
                        called_services.append(child['host.name'])
    
    return called_services
