"""
Auto-generated task-level solver.

Task ID: Task_3_11
Task Type: 6_Computation
Task Description: Identify the end-to-end response time of a given trace.
Question Template: What is the end-to-end response time of the Input Trace?
"""

def solution(trace1):
    def find_root_span(spans):
        for span in spans:
            if span['parentSpanId'] == -1:
                return span
        return None

    def dfs(span):
        if span['parentSpanId'] == -1:
            return int(span['durationTimeUnixNano'])
        for s in trace1:
            if s['spanId'] == span['parentSpanId']:
                return dfs(s) + int(span['durationTimeUnixNano'])
        return 0

    root_span = find_root_span(trace1)
    if root_span is None:
        return []
    return [dfs(root_span)]
