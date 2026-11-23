"""
Auto-generated task-level solver.

Task ID: Task_4_5
Task Type: 7_Comparison
Task Description: Identify the trace with a longer end-to-end response time between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a longer end-to-end response time?
"""

def solution(trace1, trace2):
    def get_end_to_end_time(trace):
        for span in trace:
            if span['parentSpanId'] == '-1':
                return int(span['durationTimeUnixNano'])
        return 0
    
    end_to_end_time1 = get_end_to_end_time(trace1)
    end_to_end_time2 = get_end_to_end_time(trace2)
    
    if end_to_end_time1 > end_to_end_time2:
        return trace1[0]['traceId']
    elif end_to_end_time2 > end_to_end_time1:
        return trace2[0]['traceId']
    else:
        return 'Same'
