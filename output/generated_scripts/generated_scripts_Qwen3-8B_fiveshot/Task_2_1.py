"""
Auto-generated task-level solver.

Task ID: Task_2_1
Task Type: 3_Existence
Task Description: Determine whether a specified service call pair exists in a given trace.
Question Template: Is there an HTTP call from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    # Build a map of parentSpanId to child spans
    parent_to_children = {}
    for span in trace1:
        parent_span_id = span['parentSpanId']
        if parent_span_id not in parent_to_children:
            parent_to_children[parent_span_id] = []
        parent_to_children[parent_span_id].append(span)
    
    # Check for HTTP calls from key_component_1 to key_component_2
    for span in trace1:
        if span['service.name'] == key_component_1 and span['kind'] == 'SPAN_KIND_CLIENT':
            if span['http.route'] and span['http.status_code']:
                # Check if the callee service is key_component_2
                for child_span in parent_to_children.get(span['spanId'], []):
                    if child_span['service.name'] == key_component_2 and child_span['kind'] == 'SPAN_KIND_SERVER':
                        return 'Yes'
    return 'No'
