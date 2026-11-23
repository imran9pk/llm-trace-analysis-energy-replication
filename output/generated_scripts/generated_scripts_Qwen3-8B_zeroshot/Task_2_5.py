"""
Auto-generated task-level solver.

Task ID: Task_2_5
Task Type: 4_Comparison
Task Description: Identify the span with a longer response time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer response time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def get_span_by_id(spans, span_id):
        for span in spans:
            if span['spanId'] == span_id:
                return span
        return None

    span1 = None
    span2 = None

    for span in trace1:
        if span['spanId'] == key_component_1:
            span1 = span
        if span['spanId'] == key_component_2:
            span2 = span

    if not span1 or not span2:
        return 'Invalid'

    duration1 = int(span1['durationTimeUnixNano'])
    duration2 = int(span2['durationTimeUnixNano'])

    if duration1 > duration2:
        return key_component_1
    elif duration2 > duration1:
        return key_component_2
    else:
        return 'Same'
