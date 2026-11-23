"""
Auto-generated task-level solver.

Task ID: Task_1_9
Task Type: 2_Computation
Task Description: Identify the local execution time of a given span.
Question Template: What is the local execution time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def get_span_by_id(spans, span_id):
        for span in spans:
            if span['spanId'] == span_id:
                return span
        return None

    def get_local_execution_time(span):
        if span['kind'] == 'SPAN_KIND_PRODUCER':
            return int(span['durationTimeUnixNano'])
        else:
            child_spans = [s for s in spans if s['parentSpanId'] == span['spanId']]
            total_child_duration = sum(int(s['durationTimeUnixNano']) for s in child_spans)
            return int(span['durationTimeUnixNano']) - total_child_duration

    spans = trace1
    span = get_span_by_id(spans, key_component)
    if span:
        return get_local_execution_time(span)
    else:
        return 0
