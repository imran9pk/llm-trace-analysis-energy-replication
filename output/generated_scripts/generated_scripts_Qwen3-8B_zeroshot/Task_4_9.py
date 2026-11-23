"""
Auto-generated task-level solver.

Task ID: Task_4_9
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service call pairs.
Question Template: Are the sets of service call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_call_pairs(trace):
        call_pairs = set()
        span_map = {span['spanId']: span for span in trace}
        for span in trace:
            parent_id = span['parentSpanId']
            if parent_id != -1:
                parent_span = span_map.get(parent_id)
                if parent_span:
                    call_pairs.add((parent_span['name'], span['name']))
        return call_pairs

    return 'Yes' if get_call_pairs(trace1) == get_call_pairs(trace2) else 'No'
