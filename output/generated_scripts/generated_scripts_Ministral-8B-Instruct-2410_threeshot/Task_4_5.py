"""
Auto-generated task-level solver.

Task ID: Task_4_5
Task Type: 7_Comparison
Task Description: Identify the trace with a longer end-to-end response time between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a longer end-to-end response time?
"""

def solution(trace1, trace2):
    # Extract the root span for each trace
    root_span1 = next((span for span in trace1 if span['parentSpanId'] == '-1'), None)
    root_span2 = next((span for span in trace2 if span['parentSpanId'] == '-1'), None)

    # Convert the durationTimeUnixNano to integers
    duration1 = int(root_span1['durationTimeUnixNano'])
    duration2 = int(root_span2['durationTimeUnixNano'])

    # Compare the durations
    if duration1 > duration2:
        return trace1
    elif duration2 > duration1:
        return trace2
    else:
        return 'Same'
