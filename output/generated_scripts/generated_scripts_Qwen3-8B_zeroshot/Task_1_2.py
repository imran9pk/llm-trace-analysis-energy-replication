"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    callee_services = []
    span_dict = {span['spanId']: span for span in trace1}
    for span in trace1:
        if span['service.name'] == key_component:
            parent_span_id = span['parentSpanId']
            if parent_span_id != -1:
                parent_span = span_dict.get(parent_span_id)
                if parent_span:
                    callee_services.append(parent_span['service.name'])
    return callee_services
