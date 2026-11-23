"""
Auto-generated task-level solver.

Task ID: Task_2_7
Task Type: 4_Comparison
Task Description: Identify the span with a longer local execution time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer local execution time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    spans = trace1
    span_dict = {span['spanId']: span for span in spans}
    
    def get_local_execution_time(span_id):
        span = span_dict[span_id]
        duration = int(span['durationTimeUnixNano'])
        if span['kind'] == 'SPAN_KIND_PRODUCER':
            return duration
        else:
            child_ids = [child['spanId'] for child in spans if child['parentSpanId'] == span_id]
            total_child_duration = sum(int(span_dict[child_id]['durationTimeUnixNano']) for child_id in child_ids)
            return duration - total_child_duration
    
    time1 = get_local_execution_time(key_component_1)
    time2 = get_local_execution_time(key_component_2)
    
    if time1 > time2:
        return key_component_1
    elif time2 > time1:
        return key_component_2
    else:
        return 'Same'
