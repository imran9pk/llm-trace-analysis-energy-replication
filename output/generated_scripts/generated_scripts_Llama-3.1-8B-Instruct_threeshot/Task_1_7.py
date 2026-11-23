"""
Auto-generated task-level solver.

Task ID: Task_1_7
Task Type: 2_Computation
Task Description: Identify the response time of a given span.
Question Template: What is the response time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def dfs(trace, parent_id):
        spans = {}
        for span in trace:
            spans[span['spanId']] = {'parent': parent_id, 'duration': int(span['durationTimeUnixNano'])}
        for span in trace:
            if span['parentSpanId'] == parent_id:
                dfs(trace, span['spanId'])
        return spans

    spans = dfs(trace1, -1)
    return spans.get(key_component, {}).get('duration', 0)
