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
        def dfs(span):
            nonlocal max_depth
            if span['spanId'] in visited:
                return
            visited.add(span['spanId'])
            max_depth = max(max_depth, 1 + dfs(next((s for s in trace if s['spanId'] == span['parentSpanId']), None)))
        dfs(next((s for s in trace if s['spanId'] == '-1'), None))
        return max_depth

    depth1 = get_depth(trace1)
    depth2 = get_depth(trace2)
    if depth1 > depth2:
        return next((t['traceId'] for t in trace1), '')
    elif depth2 > depth1:
        return next((t['traceId'] for t in trace2), '')
    else:
        return 'Same'
