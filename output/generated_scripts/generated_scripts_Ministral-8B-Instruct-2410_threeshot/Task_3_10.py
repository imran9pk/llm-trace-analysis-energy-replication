"""
Auto-generated task-level solver.

Task ID: Task_3_10
Task Type: 5_Existence
Task Description: Determine whether a cyclic call issue exists in a given trace.
Question Template: Is there a cyclic call issue in the Input Trace?
"""

def solution(trace1):
    from collections import defaultdict

    def build_graph(spans):
        graph = defaultdict(list)
        for span in spans:
            parent_id = int(span['parentSpanId'])
            if parent_id != -1:
                graph[parent_id].append(int(span['spanId']))
        return graph

    def has_cycle(graph, visited, rec_stack):
        for node in graph:
            if node not in visited:
                if has_cycle_recursive(graph, node, visited, rec_stack):
                    return True
        return False

    def has_cycle_recursive(graph, node, visited, rec_stack):
        if node in rec_stack:
            return True
        if node in visited:
            return False

        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph[node]:
            if has_cycle_recursive(graph, neighbor, visited, rec_stack):
                return True

        rec_stack.remove(node)
        return False

    graph = build_graph(trace1)
    visited = set()
    rec_stack = set()

    return 'Yes' if has_cycle(graph, visited, rec_stack) else 'No'
