"""
Auto-generated task-level solver.

Task ID: Task_1_5
Task Type: 1_Counting
Task Description: Identify the number of child spans of a given span.
Question Template: How many child spans does span '{key_component}' have in the Input Trace?
"""

def solution(trace1, key_component):
    parent_span_id = int(key_component)
    child_spans = [span for span in trace1 if span['parentSpanId'] == str(parent_span_id)]
    return len(child_spans)
