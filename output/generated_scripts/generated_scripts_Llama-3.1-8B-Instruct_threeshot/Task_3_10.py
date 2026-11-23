"""
Auto-generated task-level solver.

Task ID: Task_3_10
Task Type: 5_Existence
Task Description: Determine whether a cyclic call issue exists in a given trace.
Question Template: Is there a cyclic call issue in the Input Trace?
"""

def solution(trace1):
    graph = {}
    for span in trace1:
        spanId = span['spanId']
        parentSpanId = span['parentSpanId']
        if spanId not in graph:
            graph[spanId] = []
        if parentSpanId != '-1' and parentSpanId in graph:
            graph[parentSpanId].append(spanId)
        if parentSpanId == '-1':
            if spanId in graph:
                return 'Yes'
    visited = set()
    def dfs(spanId):
        if spanId in visited:
            return True
        visited.add(spanId)
        if spanId in graph:
            for child in graph[spanId]:
                if dfs(child):
                    return True
        return False
    for spanId in graph:
        if dfs(spanId):
            return 'Yes'
    return 'No'
