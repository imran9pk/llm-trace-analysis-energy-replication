"""
Auto-generated task-level solver.

Task ID: Task_2_4
Task Type: 3_Existence
Task Description: Determine whether a service instance call path from a source service instance to a destination service instance exists in a given trace.
Question Template: Is there an HTTP call path from service instance '{key_component_1}' to service instance '{key_component_2}' in the Input Trace?
"""

def solution(trace1, key_component_1, key_component_2):
    def dfs(trace, target_service):
        stack = [(span['service.name'], span['host.name']) for span in trace if span['service.name'] == target_service]
        visited = set()
        while stack:
            service, host = stack.pop()
            if (service, host) == (key_component_1, key_component_2):
                return True
            for span in trace:
                if span['service.name'] == service and span['host.name'] == host and (span['service.name'], span['host.name']) not in visited:
                    visited.add((span['service.name'], span['host.name']))
                    if span['parentSpanId'] != -1:
                        stack.append((span['service.name'], span['host.name']))
        return False

    return 'Yes' if dfs(trace1, key_component_1) else 'No'
