"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    # Build a map from service instance (host.name) to list of span IDs that belong to it
    service_to_spans = {}
    for span in trace1:
        host_name = span['host.name']
        if host_name not in service_to_spans:
            service_to_spans[host_name] = []
        service_to_spans[host_name].append(span['spanId'])
    
    # Build a map from span ID to its parent span ID
    span_id_to_parent = {}
    for span in trace1:
        span_id_to_parent[span['spanId']] = span['parentSpanId']
    
    # Find all spans that are children of the given service instance
    called_services = set()
    for span in trace1:
        if span['host.name'] == key_component:
            parent_span_id = span['spanId']
            for child_span in trace1:
                if child_span['parentSpanId'] == parent_span_id:
                    called_services.add(child_span['host.name'])
    
    return list(called_services)
