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
                parent_service = trace[int(span['parentSpanId']) - 1].get('service.name')
                if parent_service not in callers:
                    callers[parent_service] = []
                callers[parent_service].append(span['service.name'])
        return callers

    callers = get_callers(trace1)
    return [service for service in callers if key_component in callers[service]]
