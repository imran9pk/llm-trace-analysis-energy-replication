"""
Auto-generated task-level solver.

Task ID: Task_2_6
Task Type: 4_Comparison
Task Description: Identify the span with a longer waiting time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer waiting time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def get_span_waiting_time(span):
        if span['kind'] == 'SPAN_KIND_SERVER':
            return 0
        else:
            return sum(int(span['durationTimeUnixNano']) for span in trace1 if span['parentSpanId'] == span['spanId'])

    span1_waiting_time = get_span_waiting_time(next(span for span in trace1 if span['spanId'] == key_component_1))
    span2_waiting_time = get_span_waiting_time(next(span for span in trace1 if span['spanId'] == key_component_2))

    if span1_waiting_time > span2_waiting_time:
        return key_component_1
    elif span2_waiting_time > span1_waiting_time:
        return key_component_2
    else:
        return 'Same'
