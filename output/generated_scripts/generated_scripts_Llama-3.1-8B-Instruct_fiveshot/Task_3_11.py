"""
Auto-generated task-level solver.

Task ID: Task_3_11
Task Type: 6_Computation
Task Description: Identify the end-to-end response time of a given trace.
Question Template: What is the end-to-end response time of the Input Trace?
"""

def solution(trace1):
    def dfs(trace):
        root = next((span for span in trace if span['parentSpanId'] == '-1'), None)
        if root is None:
            return 0
        stack = [root]
        visited = set()
        max_duration = 0
        while stack:
            span = stack.pop()
            if span['spanId'] not in visited:
                visited.add(span['spanId'])
                max_duration = max(max_duration, int(span['durationTimeUnixNano']))
                stack.extend([s for s in trace if s['parentSpanId'] == span['spanId']])
        return max_duration

    return dfs(trace1)
