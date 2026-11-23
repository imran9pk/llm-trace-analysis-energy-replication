"""
Auto-generated task-level solver.

Task ID: Task_4_10
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instance call pairs.
Question Template: Are the sets of service instance call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def extract_service_instance_pairs(trace):
        pairs = []
        for span in trace:
            if span['parentSpanId'] != '-1':
                pairs.append((span['service.name'], span['parentSpanId']))
        return pairs

    pairs1 = extract_service_instance_pairs(trace1)
    pairs2 = extract_service_instance_pairs(trace2)

    return 'Yes' if pairs1 == pairs2 else 'No'
