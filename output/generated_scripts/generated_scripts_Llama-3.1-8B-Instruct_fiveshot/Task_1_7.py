"""
Auto-generated task-level solver.

Task ID: Task_1_7
Task Type: 2_Computation
Task Description: Identify the response time of a given span.
Question Template: What is the response time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def dfs(trace, parent_span_id):
        for span in trace:
            if span['spanId'] == key_component:
                return int(span['durationTimeUnixNano'])
            if span['parentSpanId'] == parent_span_id:
                return dfs(trace, span['spanId'])
        return None

    for span in trace1:
        if span['spanId'] == '-1':
            return dfs(trace1, span['spanId'])
