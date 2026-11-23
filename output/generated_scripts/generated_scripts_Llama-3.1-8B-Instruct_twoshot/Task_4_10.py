"""
Auto-generated task-level solver.

Task ID: Task_4_10
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instance call pairs.
Question Template: Are the sets of service instance call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

from collections import defaultdict

def solution(trace1, trace2):
    def get_service_instance_call_pairs(trace):
        service_instance_call_pairs = defaultdict(set)
        for span in trace:
            if span['parentSpanId'] != '-1':
                service_instance_call_pairs[(span['service.name'], span['parentSpanId'])].add((span['service.name'], span['spanId']))
        return service_instance_call_pairs

    trace1_service_instance_call_pairs = get_service_instance_call_pairs(trace1)
    trace2_service_instance_call_pairs = get_service_instance_call_pairs(trace2)

    return 'Yes' if trace1_service_instance_call_pairs == trace2_service_instance_call_pairs else 'No'
