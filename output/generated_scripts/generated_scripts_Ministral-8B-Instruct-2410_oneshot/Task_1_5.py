"""
Auto-generated task-level solver.

Task ID: Task_1_5
Task Type: 1_Counting
Task Description: Identify the number of child spans of a given span.
Question Template: How many child spans does span '{key_component}' have in the Input Trace?
"""

def solution(trace1, key_component):
    from collections import defaultdict

    # Create a dictionary to store spans by their parent span ID
    spans_by_parent = defaultdict(list)

    for span in trace1:
        spans_by_parent[span['parentSpanId']].append(span)

    # Find the span with the given key_component
    target_span = None
    for span in trace1:
        if span['spanId'] == key_component:
            target_span = span
            break

    if target_span is None:
        return 0

    # Count the number of child spans
    child_spans = spans_by_parent[target_span['spanId']]
    return len(child_spans)
