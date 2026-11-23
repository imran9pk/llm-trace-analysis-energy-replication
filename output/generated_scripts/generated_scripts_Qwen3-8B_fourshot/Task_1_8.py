"""
Auto-generated task-level solver.

Task ID: Task_1_8
Task Type: 2_Computation
Task Description: Identify the waiting time of a given span.
Question Template: What is the waiting time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    from collections import defaultdict

    # Build a tree structure from the trace
    tree = defaultdict(list)
    spans = {}
    for span in trace1:
        span_id = span['spanId']
        parent_span_id = span['parentSpanId']
        spans[span_id] = span
        if parent_span_id != '-1':
            tree[parent_span_id].append(span_id)

    # Calculate waiting time using DFS
    def dfs(span_id):
        span = spans[span_id]
        if span_id == span['parentSpanId'] or span['parentSpanId'] == '-1':
            return 0
        total = 0
        for child_id in tree[span_id]:
            total += dfs(child_id)
        return total

    # Find the span with the given key_component
    for span_id, span in spans.items():
        if span['spanId'] == key_component:
            return dfs(span_id)
    return 0
