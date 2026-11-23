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
            return sum(get_waiting_time(s) for s in [s for s in trace1 if s['parentSpanId'] == span['spanId']])

    trace1_dict = {s['spanId']: s for s in trace1}
    waiting_time_1 = get_waiting_time(trace1_dict[key_component_1])
    waiting_time_2 = get_waiting_time(trace1_dict[key_component_2])

    if waiting_time_1 > waiting_time_2:
        return key_component_1
    elif waiting_time_2 > waiting_time_1:
        return key_component_2
    else:
        return 'Same'
