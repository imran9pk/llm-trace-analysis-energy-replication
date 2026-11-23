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
            parent_span_id = span['parentSpanId']
            if parent_span_id == '-1':
                span_tree[span_id] = {'depth': 1, 'children': []}
            else:
                span_tree[span_id] = {'depth': 0, 'children': []}
        for span in traces:
            span_id = span['spanId']
            parent_span_id = span['parentSpanId']
            if parent_span_id != '-1':
                span_tree[parent_span_id]['children'].append(span_id)
        max_depth = 0
        for span_id in span_tree:
            depth = 1
            current_id = span_id
            while span_tree[current_id]['children']:
                depth += 1
                current_id = span_tree[current_id]['children'][0]
            max_depth = max(max_depth, depth)
        return max_depth

    depth1 = get_depth(trace1)
    depth2 = get_depth(trace2)
    if depth1 > depth2:
        return trace1[0]['traceId']
    elif depth2 > depth1:
        return trace2[0]['traceId']
    else:
        return 'Same'
