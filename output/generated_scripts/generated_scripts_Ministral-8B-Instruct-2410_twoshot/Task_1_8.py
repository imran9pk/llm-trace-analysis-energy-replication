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

    def get_child_spans(spans, parent_id):
        child_spans = []
        for span in spans:
            if span['parentSpanId'] == parent_id:
                child_spans.append(span)
        return child_spans

    def calculate_waiting_time(spans, span_id):
        span = get_span_by_id(spans, span_id)
        if span['kind'] == 'SPAN_KIND_SERVER':
            return 0
        child_spans = get_child_spans(spans, span_id)
        total_waiting_time = 0
        for child_span in child_spans:
            total_waiting_time += int(child_span['durationTimeUnixNano'])
        return total_waiting_time

    return calculate_waiting_time(trace1, key_component)
