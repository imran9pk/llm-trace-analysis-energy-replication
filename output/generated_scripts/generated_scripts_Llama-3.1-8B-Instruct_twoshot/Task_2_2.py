"""
Auto-generated task-level solver.

Task ID: Task_2_2
Task Type: 3_Existence
Task Description: Determine whether a specified service instance call pair exists in a given trace.
Question Template: Is there an HTTP call from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def find_service_instance(host_name):
        for span in trace1:
            if span['host.name'] == host_name:
                return span
        return None

    def find_parent_span_id(span_id):
        for span in trace1:
            if span['spanId'] == span_id:
                return span['parentSpanId']
        return None

    def find_child_spans(parent_span_id):
        child_spans = []
        for span in trace1:
            if span['parentSpanId'] == parent_span_id:
                child_spans.append(span)
        return child_spans

    def find_http_caller_callee(host_name_1, host_name_2):
        service_instance_1 = find_service_instance(host_name_1)
        if service_instance_1 is None:
            return False
        parent_span_id = find_parent_span_id(service_instance_1['spanId'])
        if parent_span_id is None:
            return False
        child_spans = find_child_spans(parent_span_id)
        for child_span in child_spans:
            if child_span['service.name'] == key_component_2 and child_span['host.name'] == host_name_2:
                return True
        return False

    return 'Yes' if find_http_caller_callee(key_component_1, key_component_2) else 'No'
