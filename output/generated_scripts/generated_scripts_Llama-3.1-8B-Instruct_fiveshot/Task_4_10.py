"""
Auto-generated task-level solver.

Task ID: Task_4_10
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instance call pairs.
Question Template: Are the sets of service instance call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

from collections import defaultdict

def solution(trace1, trace2):
    def get_service_call_pairs(trace):
        service_call_pairs = defaultdict(list)
        for span in trace:
            if span['parentSpanId'] != '-1':
                service_call_pairs[span['service.name']].append((span['parentSpanId'], span['spanId']))
        return service_call_pairs

    trace1_service_call_pairs = get_service_call_pairs(trace1)
    trace2_service_call_pairs = get_service_call_pairs(trace2)

    def are_service_call_pairs_equal(trace1_service_call_pairs, trace2_service_call_pairs):
        for service, call_pairs in trace1_service_call_pairs.items():
            if service not in trace2_service_call_pairs:
                return False
            for call_pair in call_pairs:
                if call_pair not in trace2_service_call_pairs[service]:
                    return False
        return True

    return 'Yes' if are_service_call_pairs_equal(trace1_service_call_pairs, trace2_service_call_pairs) else 'No'
