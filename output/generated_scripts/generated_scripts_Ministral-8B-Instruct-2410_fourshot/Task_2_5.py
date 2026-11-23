"""
Auto-generated task-level solver.

Task ID: Task_2_5
Task Type: 4_Comparison
Task Description: Identify the span with a longer response time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer response time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    span1 = next((s for s in trace1 if s['spanId'] == key_component_1), None)
    span2 = next((s for s in trace1 if s['spanId'] == key_component_2), None)

    if span1 is None or span2 is None:
        return 'Invalid span ID'

    duration1 = int(span1['durationTimeUnixNano'])
    duration2 = int(span2['durationTimeUnixNano'])

    if duration1 > duration2:
        return key_component_1
    elif duration2 > duration1:
        return key_component_2
    else:
        return 'Same'
