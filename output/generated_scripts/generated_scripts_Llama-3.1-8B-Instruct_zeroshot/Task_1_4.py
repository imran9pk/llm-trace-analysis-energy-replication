"""
Auto-generated task-level solver.

Task ID: Task_1_4
Task Type: 1_Entity
Task Description: Identify which service instances call a given service instance.
Question Template: Which service instances call the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_callers(trace, key_component):
        callers = []
        for span in trace:
            if span['name'] == key_component and span['parentSpanId'] != -1:
                for s in trace:
                    if s['spanId'] == span['parentSpanId']:
                        callers.append(s['service.name'])
        return list(set(callers))

    return get_callers(trace1, key_component)
