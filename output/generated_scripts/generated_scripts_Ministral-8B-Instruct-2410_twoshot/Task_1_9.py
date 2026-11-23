"""
Auto-generated task-level solver.

Task ID: Task_1_9
Task Type: 2_Computation
Task Description: Identify the local execution time of a given span.
Question Template: What is the local execution time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def parse_time(time_str):
        return int(time_str)

    def get_span_by_id(spans, span_id):
        for span in spans:
            if span['spanId'] == span_id:
                return span
        return None

    def get_local_execution_time(span, spans):
        if span['kind'] == 'SPAN_KIND_PRODUCER':
            return parse_time(span['durationTimeUnixNano'])
        else:
            child_spans = [s for s in spans if s['parentSpanId'] == span['spanId']]
            child_times = [get_local_execution_time(s, spans) for s in child_spans]
            return parse_time(span['durationTimeUnixNano']) - sum(child_times)

    spans = trace1
    span = get_span_by_id(spans, key_component)
    if span:
        return get_local_execution_time(span, spans)
    return 0
