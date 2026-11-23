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
        stack = [(root, root['durationTimeUnixNano'])]
        while stack:
            span, max_duration = stack.pop()
            for child in [s for s in trace if s['parentSpanId'] == span['spanId']]:
                stack.append((child, max(max_duration, int(child['durationTimeUnixNano'])))
                           )
        return max_duration

    return dfs(trace1)
