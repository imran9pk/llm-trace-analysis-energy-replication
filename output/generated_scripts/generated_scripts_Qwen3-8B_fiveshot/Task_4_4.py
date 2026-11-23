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
        
        root_spans = [span['spanId'] for span in spans if span['parentSpanId'] == '-1']
        max_depth = 0
        visited = set()
        
        for root_span in root_spans:
            stack = [(root_span, 1)]
            visited.add(root_span)
            while stack:
                current_span, depth = stack.pop()
                max_depth = max(max_depth, depth)
                for span_id, parent_id in parent_map.items():
                    if parent_id == current_span and span_id not in visited:
                        visited.add(span_id)
                        stack.append((span_id, depth + 1))
        return max_depth
    
    depth1 = get_depth(trace1)
    depth2 = get_depth(trace2)
    
    if depth1 > depth2:
        return trace1[0]['traceId']
    elif depth2 > depth1:
        return trace2[0]['traceId']
    else:
        return 'Same'
