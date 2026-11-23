"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

def solution(trace1, trace2):
    def get_depth(trace):
        from collections import defaultdict

        # Create a dictionary to store the parent-child relationships
        parent_map = defaultdict(list)
        for span in trace:
            if span['parentSpanId'] != '-1':
                parent_map[span['parentSpanId']].append(span['spanId'])

        # Use a stack to perform a depth-first search
        stack = [(span['spanId'], 0) for span in trace if span['parentSpanId'] == '-1']
        max_depth = 0

        while stack:
            current_span_id, current_depth = stack.pop()
            max_depth = max(max_depth, current_depth)
            for child_span_id in parent_map[current_span_id]:
                stack.append((child_span_id, current_depth + 1))

        return max_depth

    depth1 = get_depth(trace1)
    depth2 = get_depth(trace2)

    if depth1 > depth2:
        return trace1
    elif depth2 > depth1:
        return trace2
    else:
        return 'Same'
