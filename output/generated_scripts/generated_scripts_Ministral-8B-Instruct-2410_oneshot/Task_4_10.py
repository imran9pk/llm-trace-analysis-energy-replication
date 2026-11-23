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
        for span in trace:
            if span['parentSpanId'] != '-1':
                parent_span = next(s for s in trace if s['spanId'] == span['parentSpanId'])
                call_pairs.add((parent_span['service.name'], span['service.name']))
        return call_pairs

    return 'Yes' if get_call_pairs(trace1) == get_call_pairs(trace2) else 'No'
