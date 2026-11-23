"""
Auto-generated task-level solver.

Task ID: Task_4_10
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instance call pairs.
Question Template: Are the sets of service instance call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_call_pairs(trace):
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
        # Traverse the tree to find call pairs
        def traverse(span_id):
            if span_id not in span_tree:
                return
            span = span_tree[span_id]
            if span['parent'] is not None:
                call_pairs.add((span['parent'], span_id))
            for child_id in span['children']:
                traverse(child_id)
        # Build the children relationships
        for span in spans:
            span_id = span['spanId']
            parent_span_id = span['parentSpanId']
            if parent_span_id == '-1':
                continue
            if parent_span_id not in span_tree:
                continue
            span_tree[parent_span_id]['children'].append(span_id)
        # Traverse the tree
        traverse(next(iter(span_tree)))
        return call_pairs

    call_pairs1 = get_call_pairs(trace1)
    call_pairs2 = get_call_pairs(trace2)
    return 'Yes' if call_pairs1 == call_pairs2 else 'No'
