"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    callee_spans = []
    for span in trace1:
        if span['parentSpanId'] == key_component:
            callee_spans.append(span['service.name'])
    return callee_spans
