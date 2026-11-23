"""
Auto-generated task-level solver.

Task ID: Task_1_5
Task Type: 1_Counting
Task Description: Identify the number of child spans of a given span.
Question Template: How many child spans does span '{key_component}' have in the Input Trace?
"""

def solution(trace1, key_component):
    def count_child_spans(trace):
        child_spans = 0
        for span in trace:
            if span['parentSpanId'] == key_component:
                child_spans += 1
        return child_spans

    return count_child_spans(trace1)
