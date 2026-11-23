"""
Auto-generated task-level solver.

Task ID: Task_1_5
Task Type: 1_Counting
Task Description: Identify the number of child spans of a given span.
Question Template: How many child spans does span '{key_component}' have in the Input Trace?
"""

def solution(trace1, key_component):
    def count_child_spans(trace):
        child_count = {}
        for span in trace:
            if span['parentSpanId'] != -1:
                parent_id = span['parentSpanId']
                if parent_id not in child_count:
                    child_count[parent_id] = 0
                child_count[parent_id] += 1
        return child_count

    child_count = count_child_spans(trace1)
    return child_count.get(key_component, 0)
