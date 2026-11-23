"""
Auto-generated task-level solver.

Task ID: Task_4_5
Task Type: 7_Comparison
Task Description: Identify the trace with a longer end-to-end response time between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a longer end-to-end response time?
"""

def solution(trace1, trace2):
    def get_root_span_duration(trace):
        root_span = next(span for span in trace if span['parentSpanId'] == -1)
        return int(root_span['durationTimeUnixNano'])

    duration1 = get_root_span_duration(trace1)
    duration2 = get_root_span_duration(trace2)

    if duration1 > duration2:
        return 'Input Trace 1'
    elif duration2 > duration1:
        return 'Input Trace 2'
    else:
        return 'Same'
