"""
Auto-generated task-level solver.

Task ID: Task_1_8
Task Type: 2_Computation
Task Description: Identify the waiting time of a given span.
Question Template: What is the waiting time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_span_by_id(spans, span_id):
        for span in spans:
            if span['spanId'] == span_id:
                return span
        return None

    def calculate_waiting_time(spans, span_id):
        span = get_span_by_id(spans, span_id)
        if span['kind'] == 'PRODUCER':
            return 0
        waiting_time = 0
        for child_span in spans:
            if child_span['parentSpanId'] == span_id:
                waiting_time += int(child_span['durationTimeUnixNano'])
        return waiting_time

    root_span = next(span for span in trace1 if span['parentSpanId'] == -1)
    return calculate_waiting_time(trace1, root_span['spanId'])
