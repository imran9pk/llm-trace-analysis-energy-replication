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
            if span['parentSpanId'] != '-1':
                caller_service = trace[int(span['parentSpanId'])]['service.name']
                if span['service.name'] not in callers:
                    callers[span['service.name']] = []
                callers[span['service.name']].append(caller_service)
        return callers

    callers = get_callers(trace1)
    return [service for service in callers if key_component in callers[service]]
