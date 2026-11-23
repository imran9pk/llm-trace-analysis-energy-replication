"""
Auto-generated task-level solver.

Task ID: Task_1_9
Task Type: 2_Computation
Task Description: Identify the local execution time of a given span.
Question Template: What is the local execution time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def dfs(span):
        if span['kind'] == 'PRODUCER':
            return int(span['durationTimeUnixNano'])
        else:
            children = [s for s in trace1 if s['parentSpanId'] == span['spanId']]
            return int(span['durationTimeUnixNano']) - sum(dfs(s) for s in children)

    root_span = [s for s in trace1 if s['parentSpanId'] == -1][0]
    target_span = next((s for s in trace1 if s['name'] == key_component), None)
    if target_span is None:
        return []
    return dfs(target_span)
