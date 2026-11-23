"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_service_name(span):
        return span['service.name']

    def get_parent_service_name(span):
        parent_span_id = span['parentSpanId']
        if parent_span_id == '-1':
            return None
        for s in trace1:
            if s['spanId'] == parent_span_id:
                return get_service_name(s)
        return None

    def get_callee_services(span):
        callees = set()
        for s in trace1:
            if s['parentSpanId'] == span['spanId']:
                callees.add(get_service_name(s))
        return callees

    callees = set()
    for s in trace1:
        if get_service_name(s) == key_component:
            callees.update(get_callee_services(s))
    return list(callees)
