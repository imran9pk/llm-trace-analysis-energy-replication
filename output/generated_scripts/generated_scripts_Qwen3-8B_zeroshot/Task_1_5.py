"""
Auto-generated task-level solver.

Task ID: Task_1_5
Task Type: 1_Counting
Task Description: Identify the number of child spans of a given span.
Question Template: How many child spans does span '{key_component}' have in the Input Trace?
"""

def solution(trace1, key_component):
    span_id = None
    for span in trace1:
        if span['name'] == key_component:
            span_id = span['spanId']
            break
    if span_id is None:
        return 0
    child_count = 0
    for span in trace1:
        if span['parentSpanId'] == span_id:
            child_count += 1
    return child_count
