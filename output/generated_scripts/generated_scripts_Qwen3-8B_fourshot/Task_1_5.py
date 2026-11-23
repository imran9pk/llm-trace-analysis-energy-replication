"""
Auto-generated task-level solver.

Task ID: Task_1_5
Task Type: 1_Counting
Task Description: Identify the number of child spans of a given span.
Question Template: How many child spans does span '{key_component}' have in the Input Trace?
"""

def solution(trace1, key_component):
    span_dict = {span['spanId']: span for span in trace1}
    child_count = 0
    for span in trace1:
        if span['spanId'] == key_component:
            child_count = sum(1 for span in trace1 if span['parentSpanId'] == key_component)
            break
    return child_count
