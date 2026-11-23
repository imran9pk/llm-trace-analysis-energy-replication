"""
Auto-generated task-level solver.

Task ID: Task_4_9
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service call pairs.
Question Template: Are the sets of service call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_service_call_pairs(trace):
        service_call_pairs = set()
        for span in trace:
            if span['parentSpanId'] == -1:
                stack = [(span['spanId'], span['service.name'])]
            else:
                parent_id, parent_service = stack[-1]
                service_call_pairs.add((parent_service, span['service.name']))
                stack.append((span['spanId'], span['service.name']))
            if span['spanId'] == stack[0][0]:
                stack.pop()
        return service_call_pairs

    trace1_pairs = get_service_call_pairs(trace1)
    trace2_pairs = get_service_call_pairs(trace2)
    return 'Yes' if trace1_pairs == trace2_pairs else 'No'
