"""
Auto-generated task-level solver.

Task ID: Task_2_5
Task Type: 4_Comparison
Task Description: Identify the span with a longer response time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer response time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    spans = {}
    for span in trace1:
        spans[span['spanId']] = span['durationTimeUnixNano']
    
    duration1 = int(spans.get(key_component_1, 0))
    duration2 = int(spans.get(key_component_2, 0))
    
    if duration1 > duration2:
        return key_component_1
    elif duration2 > duration1:
        return key_component_2
    else:
        return 'Same'
