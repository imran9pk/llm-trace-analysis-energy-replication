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
            service_instances[span['service.name']].append(span['host.name'])
        return service_instances

    def get_callee_service_instances(trace, key_component):
        service_instances = get_service_instances(trace)
        key_service_name = key_component.split('-')[0]
        key_host_name = key_component.split('-')[1]
        key_service_instances = service_instances.get(key_service_name, [])
        key_host_name_in_service_instances = [host for host in key_service_instances if host == key_host_name]
        if key_host_name_in_service_instances:
            return key_service_instances
        else:
            return []

    return get_callee_service_instances(trace1, key_component)
