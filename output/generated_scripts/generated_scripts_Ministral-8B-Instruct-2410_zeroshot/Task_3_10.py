"""
Auto-generated task-level solver.

Task ID: Task_3_10
Task Type: 5_Existence
Task Description: Determine whether a cyclic call issue exists in a given trace.
Question Template: Is there a cyclic call issue in the Input Trace?
"""

def solution(trace1):
    def build_graph(spans):
        graph = {}
        for span in spans:
            span_id = span['spanId']
            parent_id = span['parentSpanId']
            if parent_id == -1:
                graph[span_id] = []
            else:
                if parent_id not in graph:
                    graph[parent_id] = []
                graph[parent_id].append(span_id)
        return graph

    def has_cycle(graph, visited, rec_stack):
        for node in graph:
            if node not in visited:
                if has_cycle_util(graph, node, visited, rec_stack):
                    return True
        return False

    def has_cycle_util(graph, node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle_util(graph, neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    graph = build_graph(trace1)
    visited = set()
    rec_stack = set()
    return 'Yes' if has_cycle(graph, visited, rec_stack) else 'No'
