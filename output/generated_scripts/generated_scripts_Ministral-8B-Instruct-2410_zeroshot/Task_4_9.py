"""
Auto-generated task-level solver.

Task ID: Task_4_9
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service call pairs.
Question Template: Are the sets of service call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_service_call_pairs(trace):
        pairs = set()
        for span in trace:
            if span['parentSpanId'] != -1:
                parent = next(s for s in trace if s['spanId'] == span['parentSpanId'])
                pairs.add((parent['service.name'], span['service.name']))
        return pairs

    return 'Yes' if get_service_call_pairs(trace1) == get_service_call_pairs(trace2) else 'No'
