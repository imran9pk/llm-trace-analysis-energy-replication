"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

def solution(trace1, trace2):
    def get_span_depth(span):
        if span['parentSpanId'] == '-1':
            return 0
        return 1 + get_span_depth(next((s for s in trace1 if s['spanId'] == span['parentSpanId']), None))

    def get_max_depth(trace):
        return max(get_span_depth(span) for span in trace)

    depth1 = get_max_depth(trace1)
    depth2 = get_max_depth(trace2)

    if depth1 > depth2:
        return trace1
    elif depth2 > depth1:
        return trace2
    else:
        return 'Same'
