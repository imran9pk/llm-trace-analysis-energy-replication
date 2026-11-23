"""
Auto-generated task-level solver.

Task ID: Task_2_7
Task Type: 4_Comparison
Task Description: Identify the span with a longer local execution time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer local execution time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def get_span_by_id(trace, span_id):
        for span in trace:
            if span['spanId'] == span_id:
                return span
        return None

    def calculate_local_execution_time(span):
        if span['kind'] == 'SPAN_KIND_SERVER':
            return int(span['durationTimeUnixNano'])
        else:
            child_spans = [s for s in trace1 if s['parentSpanId'] == span['spanId']]
            return int(span['durationTimeUnixNano']) - sum(int(c['durationTimeUnixNano']) for c in child_spans)

    span1 = get_span_by_id(trace1, key_component_1)
    span2 = get_span_by_id(trace1, key_component_2)

    if span1 is None or span2 is None:
        return 'Invalid span ID'

    local_time1 = calculate_local_execution_time(span1)
    local_time2 = calculate_local_execution_time(span2)

    if local_time1 > local_time2:
        return key_component_1
    elif local_time2 > local_time1:
        return key_component_2
    else:
        return 'Same'
