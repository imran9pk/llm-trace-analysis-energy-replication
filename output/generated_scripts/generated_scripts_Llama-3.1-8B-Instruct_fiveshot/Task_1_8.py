"""
Auto-generated task-level solver.

Task ID: Task_1_8
Task Type: 2_Computation
Task Description: Identify the waiting time of a given span.
Question Template: What is the waiting time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def dfs(span):
        if span['parentSpanId'] == '-1':
            return 0
        for s in trace1:
            if s['spanId'] == span['parentSpanId']:
                return dfs(s) + span['durationTimeUnixNano']
        return 0

    for s in trace1:
        if s['spanId'] == key_component:
            return dfs(s)
    return 0
