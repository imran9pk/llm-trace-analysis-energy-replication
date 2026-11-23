"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

def solution(trace1, trace2):
    def get_depth(trace):
        spans = trace
        parent_map = {}
        for span in spans:
            parent_map[span['spanId']] = span['parentSpanId']
        visited = set()
        max_depth = 0
        for span in spans:
            if span['parentSpanId'] == '-1':
                depth = 1
                stack = [(span['spanId'], depth)]
                while stack:
                    current_span_id, current_depth = stack.pop()
                    if current_span_id in visited:
                        continue
                    visited.add(current_span_id)
                    max_depth = max(max_depth, current_depth)
                    if current_span_id in parent_map:
                        parent_id = parent_map[current_span_id]
                        if parent_id != '-1':
                            stack.append((parent_id, current_depth + 1))
        return max_depth

    depth1 = get_depth(trace1)
    depth2 = get_depth(trace2)
    if depth1 > depth2:
        return trace1[0]['traceId']
    elif depth2 > depth1:
        return trace2[0]['traceId']
    else:
        return 'Same'
