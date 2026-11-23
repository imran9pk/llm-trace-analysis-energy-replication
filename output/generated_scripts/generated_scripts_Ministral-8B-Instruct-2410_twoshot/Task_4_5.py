"""
Auto-generated task-level solver.

Task ID: Task_4_5
Task Type: 7_Comparison
Task Description: Identify the trace with a longer end-to-end response time between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a longer end-to-end response time?
"""

def solution(trace1, trace2):
    def get_root_span_duration(trace):
        for span in trace:
            if span['parentSpanId'] == -1:
                return int(span['durationTimeUnixNano'])
        return 0

    duration1 = get_root_span_duration(trace1)
    duration2 = get_root_span_duration(trace2)

    if duration1 > duration2:
        return trace1[0]['traceId']
    elif duration2 > duration1:
        return trace2[0]['traceId']
    else:
        return 'Same'
