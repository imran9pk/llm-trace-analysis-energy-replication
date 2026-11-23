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

    def get_span_waiting_time(spans, span_id):
        span = get_span_by_id(spans, span_id)
        if span is None:
            return 0
        if span['kind'] == 'SPAN_KIND_SERVER':
            return 0
        child_spans = [s for s in spans if s['parentSpanId'] == span_id]
        return sum(int(s['durationTimeUnixNano']) for s in child_spans)

    spans = trace1
    return get_span_waiting_time(spans, key_component)
