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
        graph[spanId].append(parentSpanId)
    
    visited = set()
    recursionStack = set()
    
    def isCyclicUtil(spanId):
        if spanId in recursionStack:
            return True
        if spanId in visited:
            return False
        visited.add(spanId)
        recursionStack.add(spanId)
        if spanId in graph:
            for neighbor in graph[spanId]:
                if isCyclicUtil(neighbor):
                    return True
        recursionStack.remove(spanId)
        return False
    
    for spanId in graph:
        if isCyclicUtil(spanId):
            return 'Yes'
    return 'No'
