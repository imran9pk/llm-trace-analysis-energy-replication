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
    target_span = span_dict[key_component]
    
    if target_span['kind'] == 'SPAN_KIND_PRODUCER':
        return target_span['durationTimeUnixNano']
    
    total_child_duration = 0
    for span in spans:
        if span['parentSpanId'] == key_component:
            total_child_duration += int(span['durationTimeUnixNano'])
    
    return int(target_span['durationTimeUnixNano']) - total_child_duration
