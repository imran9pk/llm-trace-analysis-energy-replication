"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

def solution(trace1, trace2):
    def get_depth(traces):
        span_tree = {}
        for span in traces:
            span_id = span['spanId']
            parent_id = span['parentSpanId']
            if parent_id == '-1':
                span_tree[span_id] = 1
            else:
                span_tree[span_id] = span_tree.get(parent_id, 0) + 1
        return max(span_tree.values())
    
    depth1 = get_depth(trace1)
    depth2 = get_depth(trace2)
    
    if depth1 > depth2:
        return trace1[0]['traceId']
    elif depth2 > depth1:
        return trace2[0]['traceId']
    else:
        return 'Same'
