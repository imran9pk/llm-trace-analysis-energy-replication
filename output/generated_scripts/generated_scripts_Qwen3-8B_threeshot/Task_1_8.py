"""
Auto-generated task-level solver.

Task ID: Task_1_8
Task Type: 2_Computation
Task Description: Identify the waiting time of a given span.
Question Template: What is the waiting time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    spans = trace1
    span_tree = {}
    for span in spans:
        span_id = span['spanId']
        parent_id = span['parentSpanId']
        if parent_id == '-1':
            span_tree[span_id] = {'children': [], 'duration': int(span['durationTimeUnixNano'])}
        else:
            if parent_id not in span_tree:
                span_tree[parent_id] = {'children': [], 'duration': 0}
            span_tree[parent_id]['children'].append(span_id)
    
    def get_waiting_time(span_id):
        if span_id not in span_tree:
            return 0
        if span_tree[span_id]['children'] == []:
            return 0
        total = 0
        for child in span_tree[span_id]['children']:
            total += get_waiting_time(child)
        return total
    
    for span in spans:
        if span['spanId'] == key_component:
            if span['parentSpanId'] == '-1':
                return 0
            else:
                return get_waiting_time(span['spanId'])
    return 0
