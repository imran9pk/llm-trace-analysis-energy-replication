"""
Auto-generated task-level solver.

Task ID: Task_2_5
Task Type: 4_Comparison
Task Description: Identify the span with a longer response time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer response time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def get_span_id(span):
        return span['spanId']

    def get_duration(span):
        return int(span['durationTimeUnixNano'])

    def find_span(trace, key):
        for span in trace:
            if get_span_id(span) == key:
                return span
        return None

    span1 = find_span(trace1, key_component_1)
    span2 = find_span(trace1, key_component_2)

    if span1 is None or span2 is None:
        return 'Span not found'

    duration1 = get_duration(span1)
    duration2 = get_duration(span2)

    if duration1 > duration2:
        return key_component_1
    elif duration2 > duration1:
        return key_component_2
    else:
        return 'Same'
