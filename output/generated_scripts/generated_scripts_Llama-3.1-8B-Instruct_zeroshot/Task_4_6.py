"""
Auto-generated task-level solver.

Task ID: Task_4_6
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of services.
Question Template: Are the sets of services involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def get_services(trace):
        services = set()
        stack = [(span['spanId'], span['parentSpanId']) for span in trace]
        while stack:
            span_id, parent_id = stack.pop()
            for span in trace:
                if span['spanId'] == span_id:
                    services.add(span['service.name'])
                    if span['parentSpanId'] != -1:
                        stack.append((span['parentSpanId'], span['spanId']))
        return services

    trace1_services = get_services(trace1)
    trace2_services = get_services(trace2)
    return 'Yes' if trace1_services == trace2_services else 'No'
