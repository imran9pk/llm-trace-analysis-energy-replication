"""
Auto-generated task-level solver.

Task ID: Task_2_7
Task Type: 4_Comparison
Task Description: Identify the span with a longer local execution time between two given spans.
Question Template: Which span, span '{key_component_1}' or span '{key_component_2}', has a longer local execution time in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def get_local_execution_time(span):
        if span['kind'] == 'PRODUCER':
            return int(span['durationTimeUnixNano'])
        else:
            child_durations = [get_local_execution_time(s) for s in trace1 if s['parentSpanId'] == span['spanId']]
            return int(span['durationTimeUnixNano']) - sum(child_durations)

    span1 = next((s for s in trace1 if s['name'] == key_component_1), None)
    span2 = next((s for s in trace1 if s['name'] == key_component_2), None)

    if span1 is None or span2 is None:
        return 'Invalid input'

    local_time1 = get_local_execution_time(span1)
    local_time2 = get_local_execution_time(span2)

    if local_time1 > local_time2:
        return key_component_1
    elif local_time2 > local_time1:
        return key_component_2
    else:
        return 'Same'
