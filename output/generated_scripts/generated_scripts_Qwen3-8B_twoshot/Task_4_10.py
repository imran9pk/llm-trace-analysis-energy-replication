"""
Auto-generated task-level solver.

Task ID: Task_4_10
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instance call pairs.
Question Template: Are the sets of service instance call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_call_pairs(trace):
        call_pairs = set()
        spans = trace
        span_map = {span['spanId']: span for span in spans}
        for span_id, span in span_map.items():
            parent_span_id = span['parentSpanId']
            if parent_span_id != '-1':
                parent_span = span_map.get(parent_span_id)
                if parent_span:
                    parent_service = parent_span['service.name']
                    parent_host = parent_span['host.name']
                    child_service = span['service.name']
                    child_host = span['host.name']
                    call_pairs.add((parent_service, parent_host, child_service, child_host))
        return call_pairs

    call_pairs1 = get_call_pairs(trace1)
    call_pairs2 = get_call_pairs(trace2)
    return 'Yes' if call_pairs1 == call_pairs2 else 'No'
