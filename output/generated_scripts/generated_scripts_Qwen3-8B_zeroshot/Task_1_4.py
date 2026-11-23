"""
Auto-generated task-level solver.

Task ID: Task_1_4
Task Type: 1_Entity
Task Description: Identify which service instances call a given service instance.
Question Template: Which service instances call the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    callers = []
    span_dict = {span['spanId']: span for span in trace1}
    for span_id, span in span_dict.items():
        if span.get('parentSpanId') != -1 and span.get('service.name') == key_component:
            parent_span = span_dict.get(span['parentSpanId'])
            if parent_span and parent_span['service.name'] != key_component:
                callers.append(parent_span['service.name'])
    return callers
