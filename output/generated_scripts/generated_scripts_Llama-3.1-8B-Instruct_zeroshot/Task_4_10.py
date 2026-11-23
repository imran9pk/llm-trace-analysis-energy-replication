"""
Auto-generated task-level solver.

Task ID: Task_4_10
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instance call pairs.
Question Template: Are the sets of service instance call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def reconstruct_tree(trace):
        tree = {}
        for span in trace:
            span_id = int(span['spanId'])
            parent_span_id = int(span['parentSpanId'])
            if span_id not in tree:
                tree[span_id] = {'children': [], 'service_name': span['service.name'], 'host_name': span['host.name']}
            if parent_span_id != -1 and parent_span_id in tree:
                tree[parent_span_id]['children'].append(span_id)
        return tree

    def get_service_instance_call_pairs(tree):
        pairs = set()
        def dfs(node_id, path):
            if node_id in tree:
                for child_id in tree[node_id]['children']:
                    dfs(child_id, path + [node_id])
                pairs.add(tuple(sorted([tree[node_id]['service_name'], tree[node_id]['host_name']] + path)))
        dfs(0, [])  # start from the root span
        return pairs

    tree1 = reconstruct_tree(trace1)
    tree2 = reconstruct_tree(trace2)
    return 'Yes' if get_service_instance_call_pairs(tree1) == get_service_instance_call_pairs(tree2) else 'No'
