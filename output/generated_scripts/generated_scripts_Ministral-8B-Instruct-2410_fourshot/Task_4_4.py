"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

def solution(trace1, trace2):
    def get_max_depth(trace):
        max_depth = 0
        for span in trace:
            if span['parentSpanId'] == '-1':
                continue
            parent_span = next((s for s in trace if s['spanId'] == span['parentSpanId']), None)
            if parent_span is None:
                continue
            max_depth = max(max_depth, get_max_depth([parent_span]))
        return max_depth + 1

    depth1 = get_max_depth(trace1)
    depth2 = get_max_depth(trace2)

    if depth1 > depth2:
        return trace1
    elif depth2 > depth1:
        return trace2
    else:
        return "Same"
