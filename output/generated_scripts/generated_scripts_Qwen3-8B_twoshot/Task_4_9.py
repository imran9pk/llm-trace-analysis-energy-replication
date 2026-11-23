"""
Auto-generated task-level solver.

Task ID: Task_4_9
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service call pairs.
Question Template: Are the sets of service call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_service_call_pairs(trace):
        call_pairs = set()
        spans = trace
        parent_map = {}
        for span in spans:
            parent_span_id = span['parentSpanId']
            if parent_span_id != '-1':
                parent_map[span['spanId']] = parent_span_id
        for span in spans:
            parent_span_id = span['parentSpanId']
            if parent_span_id != '-1':
                call_pairs.add((span['service.name'], parent_map[span['spanId']], span['name']))
        return call_pairs

    trace1_pairs = get_service_call_pairs(trace1)
    trace2_pairs = get_service_call_pairs(trace2)
    return 'Yes' if trace1_pairs == trace2_pairs else 'No'
