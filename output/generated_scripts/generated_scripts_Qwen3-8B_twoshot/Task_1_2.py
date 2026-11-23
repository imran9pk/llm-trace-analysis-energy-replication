"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    called_services = []
    service_instances = {}
    
    for span in trace1:
        service_name = span['service.name']
        host_name = span['host.name']
        service_instance = f"{service_name}-{host_name}"
        
        if service_instance not in service_instances:
            service_instances[service_instance] = []
        
        if span['parentSpanId'] != '-1':
            parent_service_instance = None
            for parent_span in trace1:
                if parent_span['spanId'] == span['parentSpanId']:
                    parent_service_instance = f"{parent_span['service.name']}-{parent_span['host.name']}"
                    break
            
            if parent_service_instance:
                service_instances[parent_service_instance].append(service_instance)
    
    for service_instance, called_services_list in service_instances.items():
        if service_instance == key_component:
            called_services = called_services_list
    
    return called_services
