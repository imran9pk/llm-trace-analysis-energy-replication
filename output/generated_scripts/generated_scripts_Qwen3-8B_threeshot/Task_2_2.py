"""
Auto-generated task-level solver.

Task ID: Task_2_2
Task Type: 3_Existence
Task Description: Determine whether a specified service instance call pair exists in a given trace.
Question Template: Is there an HTTP call from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    # Build a map from service instance to list of spans
    service_instance_spans = {}
    for span in trace1:
        service_name = span['service.name']
        host_name = span['host.name']
        service_instance = f"{service_name}-{host_name}"
        if service_instance not in service_instance_spans:
            service_instance_spans[service_instance] = []
        service_instance_spans[service_instance].append(span)
    
    # Check for HTTP calls from key_component_1 to key_component_2
    for span in service_instance_spans.get(key_component_1, []):
        if span['kind'] == 'SPAN_KIND_CLIENT' and span.get('http.route'):
            parent_span_id = span['parentSpanId']
            if parent_span_id != '-1':
                parent_span = next((s for s in service_instance_spans.get(key_component_2, []) if s['spanId'] == parent_span_id), None)
                if parent_span and parent_span['kind'] == 'SPAN_KIND_SERVER':
                    return 'Yes'
    return 'No'
