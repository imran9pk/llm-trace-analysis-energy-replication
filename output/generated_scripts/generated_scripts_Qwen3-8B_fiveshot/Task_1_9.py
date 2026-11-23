"""
Auto-generated task-level solver.

Task ID: Task_1_9
Task Type: 2_Computation
Task Description: Identify the local execution time of a given span.
Question Template: What is the local execution time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    # Build a tree structure from the trace
    spans = trace1
    span_tree = {}
    for span in spans:
        span_id = span['spanId']
        parent_span_id = span['parentSpanId']
        if parent_span_id == '-1':
            span_tree[span_id] = {'children': [], 'duration': int(span['durationTimeUnixNano'])}
        else:
            if parent_span_id not in span_tree:
                span_tree[parent_span_id] = {'children': [], 'duration': 0}
            span_tree[parent_span_id]['children'].append(span_id)
            span_tree[span_id] = {'children': [], 'duration': int(span['durationTimeUnixNano'])}
    
    # Find the span with the given key_component
    target_span = None
    for span_id, span in span_tree.items():
        if span_id == key_component:
            target_span = span
            break
    
    if not target_span:
        return 0
    
    # Calculate the local execution time
    if target_span['children']:
        total_child_duration = sum(span_tree[child]['duration'] for child in target_span['children'])
        local_execution_time = target_span['duration'] - total_child_duration
    else:
        local_execution_time = target_span['duration']
    
    return local_execution_time
