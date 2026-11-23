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
    
    def get_local_execution_time(span_id):
        span = span_dict[span_id]
        if span['kind'] == 'SPAN_KIND_PRODUCER':
            return span['durationTimeUnixNano']
        else:
            child_ids = [child['spanId'] for child in spans if child['parentSpanId'] == span_id]
            total_child_time = sum(int(span_dict[child_id]['durationTimeUnixNano']) for child_id in child_ids)
            return int(span['durationTimeUnixNano']) - total_child_time
    
    for span in spans:
        if span['spanId'] == key_component:
            return get_local_execution_time(key_component)
    return 0
