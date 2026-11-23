"""
Auto-generated task-level solver.

Task ID: Task_1_8
Task Type: 2_Computation
Task Description: Identify the waiting time of a given span.
Question Template: What is the waiting time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    spans = trace1
    span_dict = {span['spanId']: span for span in spans}
    waiting_time = 0

    def calculate_waiting_time(span_id):
        nonlocal waiting_time
        span = span_dict[span_id]
        if span['parentSpanId'] != '-1':
            for child_id in [child['spanId'] for child in spans if child['parentSpanId'] == span_id]:
                calculate_waiting_time(child_id)
                waiting_time += int(span_dict[child_id]['durationTimeUnixNano'])

    calculate_waiting_time(key_component)
    return waiting_time
