"""
Auto-generated task-level solver.

Task ID: Task_2_7
Task Type: 4_Comparison
Task Description: Identify the span with a longer local execution time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer local execution time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def get_local_execution_time(span):
        if span['kind'] == 'SPAN_KIND_SERVER':
            return int(span['durationTimeUnixNano'])
        else:
            return int(span['durationTimeUnixNano']) - sum(int(child['durationTimeUnixNano']) for child in trace1 if child['parentSpanId'] == span['spanId'])

    span1 = next(span for span in trace1 if span['spanId'] == key_component_1)
    span2 = next(span for span in trace1 if span['spanId'] == key_component_2)

    local_time_span1 = get_local_execution_time(span1)
    local_time_span2 = get_local_execution_time(span2)

    if local_time_span1 > local_time_span2:
        return key_component_1
    elif local_time_span2 > local_time_span1:
        return key_component_2
    else:
        return 'Same'
