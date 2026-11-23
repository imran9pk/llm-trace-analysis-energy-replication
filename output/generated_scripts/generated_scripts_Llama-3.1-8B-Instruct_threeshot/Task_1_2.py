"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_service_instances(trace):
        service_instances = {}
        for span in trace:
            if span['service.name'] not in service_instances:
                service_instances[span['service.name']] = []
            service_instances[span['service.name']].append(span['spanId'])
        return service_instances

    def get_callees(trace, service_instances, key_component):
        callees = []
        for span in trace:
            if span['service.name'] == key_component and span['parentSpanId'] != '-1':
                callees.extend(service_instances[span['service.name']])
        return callees

    service_instances = get_service_instances(trace1)
    callees = get_callees(trace1, service_instances, key_component)
    return list(set(callees))
