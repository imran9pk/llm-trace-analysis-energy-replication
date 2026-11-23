"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

def solution(trace1, trace2):
    def get_span_depth(trace):
        from collections import defaultdict

        # Create a dictionary to store the parent-child relationships
        parent_map = defaultdict(list)
        for span in trace:
            parent_map[span['parentSpanId']].append(span['spanId'])

        # Initialize the depth of each span
        depth = defaultdict(int)
        for span in trace:
            if span['parentSpanId'] == '-1':
                depth[span['spanId']] = 0
            else:
                depth[span['spanId']] = depth[span['parentSpanId']] + 1

        # Find the maximum depth
        max_depth = max(depth.values())
        return max_depth

    depth1 = get_span_depth(trace1)
    depth2 = get_span_depth(trace2)

    if depth1 > depth2:
        return trace1[0]['traceId']
    elif depth2 > depth1:
        return trace2[0]['traceId']
    else:
        return 'Same'
