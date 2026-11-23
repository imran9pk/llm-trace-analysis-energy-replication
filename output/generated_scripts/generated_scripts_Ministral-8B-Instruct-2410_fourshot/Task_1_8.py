"""
Auto-generated task-level solver.

Task ID: Task_1_8
Task Type: 2_Computation
Task Description: Identify the waiting time of a given span.
Question Template: What is the waiting time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_span_by_id(trace, span_id):
        for span in trace:
            if span['spanId'] == span_id:
                return span
        return None

    def get_span_waiting_time(span):
        if span['kind'] == 'SPAN_KIND_SERVER':
            return 0
        else:
            child_spans = [s for s in trace if s['parentSpanId'] == span['spanId']]
            return sum(get_span_waiting_time(s) for s in child_spans)

    trace = trace1
    span = get_span_by_id(trace, key_component)
    if span:
        return get_span_waiting_time(span)
    else:
        return 0
