"""
Auto-generated task-level solver.

Task ID: Task_2_6
Task Type: 4_Comparison
Task Description: Identify the span with a longer waiting time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer waiting time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    spans = trace1
    span_dict = {span['spanId']: span for span in spans}
    
    def get_waiting_time(span_id):
        span = span_dict[span_id]
        if span['parentSpanId'] == '-1':
            return 0
        total = 0
        for child_id in span_dict:
            if span_dict[child_id]['parentSpanId'] == span_id:
                total += get_waiting_time(child_id)
        return total
    
    waiting_time_1 = get_waiting_time(key_component_1)
    waiting_time_2 = get_waiting_time(key_component_2)
    
    if waiting_time_1 > waiting_time_2:
        return key_component_1
    elif waiting_time_2 > waiting_time_1:
        return key_component_2
    else:
        return 'Same'
