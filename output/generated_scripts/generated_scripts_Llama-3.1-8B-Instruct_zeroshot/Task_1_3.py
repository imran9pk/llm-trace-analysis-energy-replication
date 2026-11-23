"""
Auto-generated task-level solver.

Task ID: Task_1_3
Task Type: 1_Entity
Task Description: Identify which services call a given service.
Question Template: Which services call the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_callers(trace):
        callers = set()
        for span in trace:
            if span['parentSpanId'] != -1 and span['name'] == key_component:
                callers.add(trace[span['parentSpanId']]['service.name'])
        return list(callers)

    return get_callers(trace1)
