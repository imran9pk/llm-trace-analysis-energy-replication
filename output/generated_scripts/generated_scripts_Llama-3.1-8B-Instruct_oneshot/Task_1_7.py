"""
Auto-generated task-level solver.

Task ID: Task_1_7
Task Type: 2_Computation
Task Description: Identify the response time of a given span.
Question Template: What is the response time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def dfs(span):
        if span['spanId'] == key_component:
            return int(span['durationTimeUnixNano'])
        for child in [s for s in trace1 if s['parentSpanId'] == span['spanId']]:
            result = dfs(child)
            if result:
                return result
        return None

    for span in trace1:
        result = dfs(span)
        if result:
            return result
    return None
