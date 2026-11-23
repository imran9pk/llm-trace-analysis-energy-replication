"""
Auto-generated task-level solver.

Task ID: Task_3_9
Task Type: 5_Computation
Task Description: Identify the depth of a given trace.
Question Template: What is the depth of the Input Trace?
"""

def solution(trace1):
    span_tree = {}
    for span in trace1:
        span_id = span['spanId']
        parent_span_id = span['parentSpanId']
        if parent_span_id == '-1':
            span_tree[span_id] = {'depth': 1}
        else:
            span_tree[span_id] = {'depth': span_tree[parent_span_id]['depth'] + 1}
    max_depth = max(span_tree.values(), key=lambda x: x['depth'])['depth']
    return max_depth
