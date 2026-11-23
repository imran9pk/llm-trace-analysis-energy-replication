"""
Auto-generated task-level solver.

Task ID: Task_1_3
Task Type: 1_Entity
Task Description: Identify which services call a given service.
Question Template: Which services call the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_callers(trace):
        callers = {}
        for span in trace:
            if span['parentSpanId'] != -1:
                caller_service = trace[span['parentSpanId']]['service.name']
                callee_service = span['service.name']
                if callee_service == key_component:
                    callers.setdefault(caller_service, []).append(span['spanId'])
        return callers

    callers = get_callers(trace1)
    return list(callers.keys())
