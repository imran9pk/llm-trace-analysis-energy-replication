"""
Auto-generated task-level solver.

Task ID: Task_4_10
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instance call pairs.
Question Template: Are the sets of service instance call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_span_pairs(trace):
        span_pairs = set()
        for span in trace:
            span_pairs.add((span['spanId'], span['parentSpanId']))
        return span_pairs

    return 'Yes' if get_span_pairs(trace1) == get_span_pairs(trace2) else 'No'
