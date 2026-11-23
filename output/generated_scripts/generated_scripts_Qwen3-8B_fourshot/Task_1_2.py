"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    service_instances = set()
    for span in trace1:
        if span['service.name'] == key_component:
            if 'parentSpanId' in span:
                parent_span_id = span['parentSpanId']
                for other_span in trace1:
                    if other_span['spanId'] == parent_span_id:
                        service_instances.add(other_span['service.name'])
    return list(service_instances)
