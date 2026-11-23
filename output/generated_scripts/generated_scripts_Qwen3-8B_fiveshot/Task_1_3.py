"""
Auto-generated task-level solver.

Task ID: Task_1_3
Task Type: 1_Entity
Task Description: Identify which services call a given service.
Question Template: Which services call the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    caller_services = set()
    service_map = {}
    for span in trace1:
        service_name = span['service.name']
        if service_name not in service_map:
            service_map[service_name] = []
        service_map[service_name].append(span['spanId'])
    
    for span in trace1:
        parent_span_id = span['parentSpanId']
        if parent_span_id != '-1':
            parent_service_name = None
            for service, span_ids in service_map.items():
                if span['spanId'] in span_ids:
                    parent_service_name = service
                    break
            if parent_service_name and parent_service_name != key_component:
                caller_services.add(parent_service_name)
    
    return list(caller_services)
