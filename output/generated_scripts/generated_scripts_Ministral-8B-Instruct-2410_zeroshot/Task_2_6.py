"""
Auto-generated task-level solver.

Task ID: Task_2_6
Task Type: 4_Comparison
Task Description: Identify the span with a longer waiting time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer waiting time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def calculate_waiting_time(span):
        if span['kind'] == 'PRODUCER':
            return 0
        return sum(child['durationTimeUnixNano'] for child in trace1 if child['parentSpanId'] == span['spanId'])

    def find_span_by_name(trace, name):
        for span in trace:
            if span['name'] == name:
                return span
        return None

    span1 = find_span_by_name(trace1, key_component_1)
    span2 = find_span_by_name(trace1, key_component_2)

    if span1 is None or span2 is None:
        return 'Invalid span names'

    waiting_time1 = calculate_waiting_time(span1)
    waiting_time2 = calculate_waiting_time(span2)

    if waiting_time1 > waiting_time2:
        return key_component_1
    elif waiting_time2 > waiting_time1:
        return key_component_2
    else:
        return 'Same'
