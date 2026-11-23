"""
Auto-generated task-level solver.

Task ID: Task_3_9
Task Type: 5_Computation
Task Description: Identify the depth of a given trace.
Question Template: What is the depth of the Input Trace?
"""

def solution(trace1):
    from collections import defaultdict

    def get_depth(span, parent_map):
        if span['parentSpanId'] == -1:
            return 0
        return 1 + get_depth(parent_map[span['parentSpanId']], parent_map)

    parent_map = defaultdict(list)
    for span in trace1:
        parent_map[span['spanId']].append(span)

    max_depth = 0
    for span in trace1:
        if span['parentSpanId'] == -1:
            max_depth = max(max_depth, get_depth(span, parent_map))

    return max_depth
