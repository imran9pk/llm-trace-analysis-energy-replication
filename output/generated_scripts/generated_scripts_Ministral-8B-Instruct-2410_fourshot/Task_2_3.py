"""
Auto-generated task-level solver.

Task ID: Task_2_3
Task Type: 3_Existence
Task Description: Determine whether a service call path from a source service to a destination service exists in a given trace.
Question Template: Is there an HTTP call path from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def find_path(spans, src, dest):
        stack = [(src, -1)]
        while stack:
            current, parent = stack.pop()
            if current['service.name'] == dest:
                return True
            for span in spans:
                if span['parentSpanId'] == current['spanId']:
                    stack.append((span, current['spanId']))
        return False

    for span in trace1:
        if span['service.name'] == key_component_1:
            if find_path(trace1, span, key_component_2):
                return 'Yes'
    return 'No'
