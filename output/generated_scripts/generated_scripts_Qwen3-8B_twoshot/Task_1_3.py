"""
Auto-generated task-level solver.

Task ID: Task_1_3
Task Type: 1_Entity
Task Description: Identify which services call a given service.
Question Template: Which services call the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    caller_services = set()
    service_name_to_callers = {}
    
    for span in trace1:
        service_name = span['service.name']
        parent_span_id = span['parentSpanId']
        
        if parent_span_id != '-1':
            if service_name not in service_name_to_callers:
                service_name_to_callers[service_name] = set()
            service_name_to_callers[service_name].add(span['service.name'])
    
    if key_component in service_name_to_callers:
        return list(service_name_to_callers[key_component])
    else:
        return []
