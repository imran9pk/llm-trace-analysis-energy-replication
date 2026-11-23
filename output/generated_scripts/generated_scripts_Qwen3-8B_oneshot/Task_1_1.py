"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    called_services = set()
    seen_span_ids = set()
    
    for span in trace1:
        span_id = span['spanId']
        parent_span_id = span['parentSpanId']
        
        if span_id in seen_span_ids:
            continue
        seen_span_ids.add(span_id)
        
        if parent_span_id != '-1':
            parent_span = next((s for s in trace1 if s['spanId'] == parent_span_id), None)
            if parent_span and parent_span['service.name'] == key_component:
                called_services.add(span['service.name'])
    
    return list(called_services)
