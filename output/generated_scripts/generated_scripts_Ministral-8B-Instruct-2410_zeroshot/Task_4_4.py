"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

def solution(trace1, trace2):
    def get_span_tree(trace):
        from collections import defaultdict

        tree = defaultdict(list)
        for span in trace:
            span_id = span['spanId']
            parent_span_id = span['parentSpanId']
            if parent_span_id == -1:
                root = span_id
            else:
                tree[parent_span_id].append(span_id)
        return tree, root

    def get_max_depth(tree, root):
        def dfs(span_id, depth):
            if span_id not in tree:
                return depth
            max_depth = depth
            for child in tree[span_id]:
                max_depth = max(max_depth, dfs(child, depth + 1))
            return max_depth

        return dfs(root, 0)

    tree1, root1 = get_span_tree(trace1)
    tree2, root2 = get_span_tree(trace2)

    depth1 = get_max_depth(tree1, root1)
    depth2 = get_max_depth(tree2, root2)

    if depth1 > depth2:
        return 'Input Trace 1'
    elif depth2 > depth1:
        return 'Input Trace 2'
    else:
        return 'Same'
