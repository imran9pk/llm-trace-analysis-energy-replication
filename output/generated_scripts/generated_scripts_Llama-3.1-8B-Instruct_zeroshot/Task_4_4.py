"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

def solution(trace1, trace2):
    def get_depth(trace):
        max_depth = 0
        visited = set()
        for span in trace:
            stack = [(span['spanId'], 1)]
            while stack:
                span_id, depth = stack.pop()
                if span_id not in visited:
                    visited.add(span_id)
                    if span_id != -1:
                        parent_span_id = next((s['spanId'] for s in trace if s['parentSpanId'] == span_id), None)
                        if parent_span_id is not None:
                            stack.append((parent_span_id, depth + 1))
                    max_depth = max(max_depth, depth)
        return max_depth

    depth1 = get_depth(trace1)
    depth2 = get_depth(trace2)
    if depth1 > depth2:
        return 'Input Trace 1'
    elif depth2 > depth1:
        return 'Input Trace 2'
    else:
        return 'Same'
