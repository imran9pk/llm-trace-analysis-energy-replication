"""
Auto-generated task-level solver.

Task ID: Task_1_7
Task Type: 2_Computation
Task Description: Identify the response time of a given span.
Question Template: What is the response time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def find_span(trace, key_component):
        for span in trace:
            if span['name'] == key_component:
                return span
        return None

    def get_response_time(span):
        return int(span['endTimeUnixNano']) - int(span['startTimeUnixNano'])

    span = find_span(trace1, key_component)
    if span:
        return get_response_time(span)
    else:
        return []
