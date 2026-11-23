"""
Auto-generated task-level solver.

Task ID: Task_2_3
Task Type: 3_Existence
Task Description: Determine whether a service call path from a source service to a destination service exists in a given trace.
Question Template: Is there an HTTP call path from service '{key_component_1}' to service '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def find_path(spans, src, dest):
        if not spans:
            return False
        for span in spans:
            if span['service.name'] == src:
                for child in spans:
                    if child['parentSpanId'] == span['spanId']:
                        if child['service.name'] == dest:
                            return True
                        if find_path([child], src, dest):
                            return True
        return False

    return 'Yes' if find_path(trace1, key_component_1, key_component_2) else 'No'
