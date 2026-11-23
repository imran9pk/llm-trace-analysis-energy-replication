"""
Auto-generated task-level solver.

Task ID: Task_4_5
Task Type: 7_Comparison
Task Description: Identify the trace with a longer end-to-end response time between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a longer end-to-end response time?
"""

def solution(trace1, trace2):
    def get_root_span(trace):
        for span in trace:
            if span['parentSpanId'] == '-1':
                return span
        return None

    def get_end_to_end_response_time(trace):
        root_span = get_root_span(trace)
        if root_span is None:
            return 0
        return int(root_span['durationTimeUnixNano'])

    trace1_end_to_end_response_time = get_end_to_end_response_time(trace1)
    trace2_end_to_end_response_time = get_end_to_end_response_time(trace2)

    if trace1_end_to_end_response_time > trace2_end_to_end_response_time:
        return '/hpersR+7AKgTUaRYZ78zQ=='
    elif trace2_end_to_end_response_time > trace1_end_to_end_response_time:
        return 'fcxENQeHy5PHAPjDLixRYA=='
    else:
        return 'Same'
