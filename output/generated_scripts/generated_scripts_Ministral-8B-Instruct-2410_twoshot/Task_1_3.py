"""
Auto-generated task-level solver.

Task ID: Task_1_3
Task Type: 1_Entity
Task Description: Identify which services call a given service.
Question Template: Which services call the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    callers = []
    for span in trace1:
        if span['service.name'] == key_component:
            parent_span = next((s for s in trace1 if s['spanId'] == span['parentSpanId']), None)
            if parent_span:
                callers.append(parent_span['service.name'])
    return list(set(callers))
