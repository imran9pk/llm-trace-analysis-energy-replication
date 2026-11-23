"""
Auto-generated task-level solver.

Task ID: Task_3_9
Task Type: 5_Computation
Task Description: Identify the depth of a given trace.
Question Template: What is the depth of the Input Trace?
"""

def solution(trace1):
    from collections import defaultdict

    def get_span_depth(span, parent_span_id):
        if span['parentSpanId'] == -1:
            return 1
        for s in trace1:
            if s['spanId'] == span['parentSpanId']:
                return 1 + get_span_depth(s, parent_span_id)
        return 0

    max_depth = 0
    for span in trace1:
        if span['parentSpanId'] == -1:
            max_depth = max(max_depth, get_span_depth(span, span['spanId']))

    return max_depth
