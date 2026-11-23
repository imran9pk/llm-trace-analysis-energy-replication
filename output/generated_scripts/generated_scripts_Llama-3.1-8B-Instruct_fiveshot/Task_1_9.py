"""
Auto-generated task-level solver.

Task ID: Task_1_9
Task Type: 2_Computation
Task Description: Identify the local execution time of a given span.
Question Template: What is the local execution time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def dfs(span):
        if span['kind'] == 'SPAN_KIND_PRODUCER':
            return span['durationTimeUnixNano']
        else:
            children = [s for s in trace1 if s['parentSpanId'] == span['spanId']]
            return span['durationTimeUnixNano'] - sum(dfs(s) for s in children)

    return dfs(next(s for s in trace1 if s['spanId'] == key_component))
