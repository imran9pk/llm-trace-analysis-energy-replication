"""
Auto-generated task-level solver.

Task ID: Task_2_4
Task Type: 3_Existence
Task Description: Determine whether a service instance call path from a source service instance to a destination service instance exists in a given trace.
Question Template: Is there an HTTP call path from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def find_path(spans, src, dest):
        if not spans:
            return False
        for span in spans:
            if span['service.name'] == src and span['http.status_code'] == '200':
                if span['parentSpanId'] == -1:
                    return True
                return find_path([s for s in spans if s['spanId'] == span['parentSpanId']], dest, dest)
        return False

    return 'Yes' if find_path(trace1, key_component_1, key_component_2) else 'No'
