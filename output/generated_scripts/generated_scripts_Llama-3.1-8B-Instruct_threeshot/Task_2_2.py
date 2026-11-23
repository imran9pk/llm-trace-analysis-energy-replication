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

    def is_http_call(span):
        return span['name'].startswith('HTTP ') or span['name'].startswith('/api/')

    def is_service_instance(span, key_component):
        return span['service.name'] == key_component

    def dfs(span_id):
        if span_id is None:
            return False
        span = find_service_instance(trace1[0]['host.name'])
        if span is None:
            return False
        if is_service_instance(span, key_component_1) and is_service_instance(find_service_instance(trace1[0]['host.name']), key_component_2) and is_http_call(span):
            return True
        child_spans = find_child_spans(span_id)
        for child_span in child_spans:
            if dfs(child_span['spanId']):
                return True
        return False

    return 'Yes' if dfs('-1') else 'No'
