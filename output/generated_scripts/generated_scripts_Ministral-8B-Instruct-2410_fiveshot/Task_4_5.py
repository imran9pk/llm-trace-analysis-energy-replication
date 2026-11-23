"""
Auto-generated task-level solver.

Task ID: Task_4_5
Task Type: 7_Comparison
Task Description: Identify the trace with a longer end-to-end response time between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a longer end-to-end response time?
"""

def solution(trace1, trace2):
    # Extract the root span of each trace
    root_span1 = next((span for span in trace1 if span['parentSpanId'] == -1), None)
    root_span2 = next((span for span in trace2 if span['parentSpanId'] == -1), None)

    # Calculate the end-to-end response time for each trace
    end_to_end_time1 = int(root_span1['endTimeUnixNano']) - int(root_span1['startTimeUnixNano'])
    end_to_end_time2 = int(root_span2['endTimeUnixNano']) - int(root_span2['startTimeUnixNano'])

    # Compare the end-to-end response times
    if end_to_end_time1 > end_to_end_time2:
        return trace1
    elif end_to_end_time2 > end_to_end_time1:
        return trace2
    else:
        return "Same"
