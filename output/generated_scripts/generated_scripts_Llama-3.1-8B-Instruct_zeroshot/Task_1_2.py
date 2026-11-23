"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_callees(trace, key_component):
        callees = []
        for span in trace:
            if span['parentSpanId'] == span['spanId']:
                continue
            if span['parentSpanId'] == -1:
                continue
            if span['service.name'] == key_component:
                callees.append(span['spanId'])
        return callees

    return get_callees(trace1, key_component)
