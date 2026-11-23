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
        # Traverse the tree to find call pairs
        def traverse(span_id):
            if span_id not in span_tree:
                return
            span = span_tree[span_id]
            if span['parent'] is not None:
                call_pairs.add((span['parent'], span_id))
            for child_id in span['children']:
                traverse(child_id)
        traverse(list(span_tree.keys())[0])
        return call_pairs

    call_pairs1 = get_service_call_pairs(trace1)
    call_pairs2 = get_service_call_pairs(trace2)
    return 'Yes' if call_pairs1 == call_pairs2 else 'No'
