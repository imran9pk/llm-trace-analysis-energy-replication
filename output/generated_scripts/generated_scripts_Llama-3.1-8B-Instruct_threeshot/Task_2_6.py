"""
Auto-generated task-level solver.

Task ID: Task_2_6
Task Type: 4_Comparison
Task Description: Identify the span with a longer waiting time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer waiting time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def get_waiting_time(span):
        if span['parentSpanId'] == '-1':
            return 0
        else:
            return sum(get_waiting_time(s) for s in trace1 if s['parentSpanId'] == span['spanId'])

    def get_span_id(span):
        return span['spanId']

    span1 = next((s for s in trace1 if get_span_id(s) == key_component_1), None)
    span2 = next((s for s in trace1 if get_span_id(s) == key_component_2), None)

    if span1 is None or span2 is None:
        return 'Invalid span ID'

    return key_component_1 if get_waiting_time(span1) > get_waiting_time(span2) else key_component_2 if get_waiting_time(span2) > get_waiting_time(span1) else 'Same'
