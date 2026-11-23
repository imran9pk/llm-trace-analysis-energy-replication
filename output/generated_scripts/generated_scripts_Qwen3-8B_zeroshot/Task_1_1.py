"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    called_services = []
    span_dict = {span['spanId']: span for span in trace1}
    for span in trace1:
        if span['service.name'] == key_component:
            parent_span_id = span['parentSpanId']
            if parent_span_id != -1:
                parent_span = span_dict.get(parent_span_id)
                if parent_span and parent_span['service.name'] not in called_services:
                    called_services.append(parent_span['service.name'])
    return called_services
