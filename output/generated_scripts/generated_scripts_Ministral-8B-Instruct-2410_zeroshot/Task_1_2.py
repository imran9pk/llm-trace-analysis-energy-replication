"""
Auto-generated task-level solver.

Task ID: Task_1_2
Task Type: 1_Entity
Task Description: Identify which service instances are called by a given service instance.
Question Template: Which service instances are called by the service instance '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_callees(spans, key_component):
        callee_spans = []
        for span in spans:
            if span['parentSpanId'] == -1:
                continue
            if span['service.name'] == key_component:
                callee_spans.append(span['service.name'])
        return callee_spans

    def find_span_by_id(spans, span_id):
        for span in spans:
            if span['spanId'] == span_id:
                return span
        return None

    def build_span_tree(spans):
        span_tree = {}
        for span in spans:
            span_id = span['spanId']
            parent_id = span['parentSpanId']
            if parent_id == -1:
                span_tree[span_id] = []
            else:
                if parent_id not in span_tree:
                    span_tree[parent_id] = []
                span_tree[parent_id].append(span_id)
        return span_tree

    span_tree = build_span_tree(trace1)
    callee_spans = get_callees(trace1, key_component)
    return callee_spans
