"""
Auto-generated task-level solver.

Task ID: Task_1_5
Task Type: 1_Counting
Task Description: Identify the number of child spans of a given span.
Question Template: How many child spans does span '{key_component}' have in the Input Trace?
"""

def solution(trace1, key_component):
    def dfs(span_id):
        count = 0
        for span in trace1:
            if span['parentSpanId'] == span_id:
                count += 1
                count += dfs(span['spanId'])
        return count

    return dfs(key_component)
