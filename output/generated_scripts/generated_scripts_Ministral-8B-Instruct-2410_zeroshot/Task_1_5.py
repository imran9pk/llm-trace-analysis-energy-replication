"""
Auto-generated task-level solver.

Task ID: Task_1_5
Task Type: 1_Counting
Task Description: Identify the number of child spans of a given span.
Question Template: How many child spans does span '{key_component}' have in the Input Trace?
"""

def solution(trace1, key_component):
    def get_span_id(span):
        return span['spanId']

    def get_parent_span_id(span):
        return span['parentSpanId']

    def find_span_by_id(trace, span_id):
        for span in trace:
            if get_span_id(span) == span_id:
                return span
        return None

    def count_child_spans(trace, parent_span_id):
        count = 0
        for span in trace:
            if get_parent_span_id(span) == parent_span_id:
                count += 1
                count += count_child_spans(trace, get_span_id(span))
        return count

    parent_span = find_span_by_id(trace1, key_component)
    if parent_span is None:
        return 0

    return count_child_spans(trace1, get_span_id(parent_span))
