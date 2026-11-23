"""
Auto-generated task-level solver.

Task ID: Task_1_9
Task Type: 2_Computation
Task Description: Identify the local execution time of a given span.
Question Template: What is the local execution time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    spans = trace1
    span_dict = {span['spanId']: span for span in spans}
    total_duration = int(span_dict[key_component]['durationTimeUnixNano'])
    parent_span_id = span_dict[key_component]['parentSpanId']
    
    if parent_span_id == -1:
        return total_duration
    
    child_spans = [span for span in spans if span['parentSpanId'] == key_component]
    child_durations = sum(int(span['durationTimeUnixNano']) for span in child_spans)
    
    return total_duration - child_durations
