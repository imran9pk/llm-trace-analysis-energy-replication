"""
Auto-generated task-level solver.

Task ID: Task_1_3
Task Type: 1_Entity
Task Description: Identify which services call a given service.
Question Template: Which services call the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    callers = []
    span_dict = {span['spanId']: span for span in trace1}
    for span in trace1:
        if span['service.name'] == key_component:
            parent_span_id = span['parentSpanId']
            if parent_span_id != -1:
                parent_span = span_dict.get(parent_span_id)
                if parent_span and parent_span['service.name'] != key_component:
                    callers.append(parent_span['service.name'])
    return callers
