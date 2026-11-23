"""
Auto-generated task-level solver.

Task ID: Task_1_4
Task Type: 1_Entity
Task Description: Identify which service instances call a given service instance.
Question Template: Which service instances call the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    callers = []
    for span in trace1:
        if span['spanId'] == key_component:
            parent_span = next((s for s in trace1 if s['spanId'] == span['parentSpanId']), None)
            if parent_span:
                callers.append(parent_span['service.name'])
    return callers
