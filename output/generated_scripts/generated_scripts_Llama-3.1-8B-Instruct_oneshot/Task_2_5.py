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
        spans[span['spanId']] = {'duration': int(span['durationTimeUnixNano']), 'parent': span['parentSpanId']}
    
    def dfs(span_id):
        if span_id == -1:
            return 0
        return dfs(spans[span_id]['parent']) + spans[span_id]['duration']
    
    duration1 = dfs(int(key_component_1))
    duration2 = dfs(int(key_component_2))
    
    if duration1 > duration2:
        return key_component_1
    elif duration2 > duration1:
        return key_component_2
    else:
        return 'Same'
