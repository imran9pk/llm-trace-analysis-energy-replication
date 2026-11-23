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
    key_span = next((s for s in trace1 if s['spanId'] == key_component), None)

    if key_span is None:
        return 0

    # Get the list of child spans for the key span
    child_spans = spans_by_parent[key_span['spanId']]

    return len(child_spans)
