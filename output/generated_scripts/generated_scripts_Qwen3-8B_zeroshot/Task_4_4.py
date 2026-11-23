"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

def solution(trace1, trace2):
    def get_max_depth(traces):
        span_map = {}
        for span in traces:
            span_id = span['spanId']
            parent_id = span['parentSpanId']
            span_map[span_id] = parent_id
        depth = 0
        visited = set()
        for span_id in span_map:
            if span_id not in visited:
                stack = [(span_id, 0)]
                while stack:
                    current_id, current_depth = stack.pop()
                    if current_id in visited:
                        continue
                    visited.add(current_id)
                    if current_depth > depth:
                        depth = current_depth
                    parent_id = span_map.get(current_id, -1)
                    if parent_id != -1 and parent_id not in visited:
                        stack.append((parent_id, current_depth + 1))
        return depth

    depth1 = get_max_depth(trace1)
    depth2 = get_max_depth(trace2)
    if depth1 > depth2:
        return 1
    elif depth2 > depth1:
        return 2
    else:
        return "Same"
