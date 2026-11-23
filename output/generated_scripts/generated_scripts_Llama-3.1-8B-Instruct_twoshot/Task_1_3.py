"""
Auto-generated task-level solver.

Task ID: Task_1_3
Task Type: 1_Entity
Task Description: Identify which services call a given service.
Question Template: Which services call the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_caller_services(trace):
        caller_services = set()
        for span in trace:
            if span['parentSpanId'] != '-1' and span['service.name'] != key_component:
                caller_services.add(span['service.name'])
        return list(caller_services)

    return get_caller_services(trace1)
