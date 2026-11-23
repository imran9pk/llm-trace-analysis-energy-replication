"""
Auto-generated task-level solver.

Task ID: Task_3_11
Task Type: 6_Computation
Task Description: Identify the end-to-end response time of a given trace.
Question Template: What is the end-to-end response time of the Input Trace?
"""

def solution(trace1):
    def find_root_span(trace):
        for span in trace:
            if span['parentSpanId'] == '-1':
                return span
        return None

    def dfs(trace, root_span_id):
        root_span = next((span for span in trace if span['spanId'] == root_span_id), None)
        if root_span is None:
            return 0
        return root_span['durationTimeUnixNano']

    root_span = find_root_span(trace1)
    if root_span is None:
        return 0
    return dfs(trace1, root_span['spanId'])
