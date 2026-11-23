"""
Auto-generated task-level solver.

Task ID: Task_2_7
Task Type: 4_Comparison
Task Description: Identify the span with a longer local execution time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer local execution time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def get_local_execution_time(span):
        if span['kind'] == 'SPAN_KIND_SERVER':
            return int(span['durationTimeUnixNano'])
        else:
            total_child_duration = 0
            for child in [s for s in trace1 if s['parentSpanId'] == span['spanId']]:
                total_child_duration += get_local_execution_time(child)
            return int(span['durationTimeUnixNano']) - total_child_duration

    span1 = next((s for s in trace1 if s['spanId'] == key_component_1), None)
    span2 = next((s for s in trace1 if s['spanId'] == key_component_2), None)
    
    if span1 is None or span2 is None:
        return 'Invalid span ID'
    
    local_time1 = get_local_execution_time(span1)
    local_time2 = get_local_execution_time(span2)
    
    if local_time1 > local_time2:
        return key_component_1
    elif local_time2 > local_time1:
        return key_component_2
    else:
        return 'Same'
