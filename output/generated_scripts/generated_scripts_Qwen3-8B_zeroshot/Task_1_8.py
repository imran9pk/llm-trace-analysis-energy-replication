"""
Auto-generated task-level solver.

Task ID: Task_1_8
Task Type: 2_Computation
Task Description: Identify the waiting time of a given span.
Question Template: What is the waiting time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    from collections import defaultdict

    span_tree = defaultdict(list)
    span_dict = {}
    for span in trace1:
        span_id = span['spanId']
        parent_id = span['parentSpanId']
        span_dict[span_id] = span
        if parent_id != -1:
            span_tree[parent_id].append(span_id)

    def get_waiting_time(span_id):
        span = span_dict[span_id]
        if span['kind'] == 'PRODUCER':
            return 0
        total = 0
        for child_id in span_tree[span_id]:
            total += get_waiting_time(child_id)
        return total

    return get_waiting_time(key_component)
