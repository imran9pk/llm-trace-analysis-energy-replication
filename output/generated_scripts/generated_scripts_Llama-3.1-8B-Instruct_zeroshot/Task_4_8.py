"""
Auto-generated task-level solver.

Task ID: Task_4_8
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of operations.
Question Template: Are the sets of operations involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def reconstruct_tree(trace):
        tree = {}
        for span in trace:
            span_id = int(span['spanId'])
            parent_span_id = int(span['parentSpanId'])
            if span_id not in tree:
                tree[span_id] = {'children': [], 'name': span['name'], 'kind': span['kind']}
            if parent_span_id != -1 and parent_span_id in tree:
                tree[parent_span_id]['children'].append(span_id)
        return tree

    def is_same_tree(tree1, tree2):
        if set(tree1.keys()) != set(tree2.keys()):
            return False
        for span_id in tree1:
            if tree1[span_id]['name'] != tree2[span_id]['name'] or tree1[span_id]['kind'] != tree2[span_id]['kind']:
                return False
            if tree1[span_id]['children'] != tree2[span_id]['children']:
                return False
            if tree1[span_id]['children']:
                if not is_same_tree({child: tree1[child] for child in tree1[span_id]['children']}, {child: tree2[child] for child in tree2[span_id]['children']}):
                    return False
        return True

    tree1 = reconstruct_tree(trace1)
    tree2 = reconstruct_tree(trace2)
    return 'Yes' if is_same_tree(tree1, tree2) else 'No'
