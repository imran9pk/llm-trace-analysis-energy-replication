"""
Auto-generated task-level solver.

Task ID: Task_4_9
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service call pairs.
Question Template: Are the sets of service call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_service_call_pairs(trace):
        call_pairs = set()
        spans = trace
        # Build the tree structure
        span_tree = {}
        for span in spans:
            span_id = span['spanId']
            parent_span_id = span['parentSpanId']
            if parent_span_id == '-1':
                span_tree[span_id] = {'parent': None, 'children': []}
            else:
                span_tree[span_id] = {'parent': parent_span_id, 'children': []}
        # Build the tree
        for span in spans:
            span_id = span['spanId']
            parent_span_id = span['parentSpanId']
            if parent_span_id != '-1':
                span_tree[parent_span_id]['children'].append(span_id)
        # Traverse the tree to find call pairs
        def traverse(span_id):
            if span_id not in span_tree:
                return
            span = next(s for s in spans if s['spanId'] == span_id)
            parent_span = span_tree[span_id]['parent']
            if parent_span is not None:
                parent = next(s for s in spans if s['spanId'] == parent_span)
                call_pairs.add((parent['service.name'], span['service.name']))
            for child in span_tree[span_id]['children']:
                traverse(child)
        traverse(next(s for s in spans if s['parentSpanId'] == '-1')['spanId'])
        return call_pairs
    call_pairs1 = get_service_call_pairs(trace1)
    call_pairs2 = get_service_call_pairs(trace2)
    return 'Yes' if call_pairs1 == call_pairs2 else 'No'
