"""
Auto-generated task-level solver.

Task ID: Task_2_2
Task Type: 3_Existence
Task Description: Determine whether a specified service instance call pair exists in a given trace.
Question Template: Is there an HTTP call from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    caller_service_instances = set()
    callee_service_instances = set()
    
    for span in trace1:
        if span['kind'] == 'SPAN_KIND_CLIENT':
            caller_service_instances.add(span['service.name'] + ':' + span['host.name'])
        elif span['kind'] == 'SPAN_KIND_SERVER':
            callee_service_instances.add(span['service.name'] + ':' + span['host.name'])
    
    caller_service = key_component_1
    callee_service = key_component_2
    
    if caller_service in caller_service_instances and callee_service in callee_service_instances:
        return 'Yes'
    else:
        return 'No'
