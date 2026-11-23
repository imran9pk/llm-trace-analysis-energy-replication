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
            parent_id = span['parentSpanId']
            if parent_id == '-1':
                span_tree[span_id] = {'parent': None, 'children': []}
            else:
                span_tree[span_id] = {'parent': parent_id, 'children': []}
        # Traverse the tree to collect call pairs
        def traverse(span_id):
            if span_id not in span_tree:
                return
            span = span_tree[span_id]
            if span['parent'] is not None:
                call_pairs.add((span['parent'], span_id))
            for child_id in span['children']:
                traverse(child_id)
        # Build children relationships
        for span in spans:
            span_id = span['spanId']
            parent_id = span['parentSpanId']
            if parent_id != '-1':
                span_tree[parent_id]['children'].append(span_id)
        # Traverse the tree
        traverse(next(iter(span_tree)))
        return call_pairs

    trace1_pairs = get_service_call_pairs(trace1)
    trace2_pairs = get_service_call_pairs(trace2)
    return 'Yes' if trace1_pairs == trace2_pairs else 'No'
