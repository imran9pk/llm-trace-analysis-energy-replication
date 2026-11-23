"""
Auto-generated task-level solver.

Task ID: Task_3_10
Task Type: 5_Existence
Task Description: Determine whether a cyclic call issue exists in a given trace.
Question Template: Is there a cyclic call issue in the Input Trace?
"""

from collections import defaultdict, deque

def solution(trace1):
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    for span in trace1:
        spanId = span['spanId']
        parentSpanId = span['parentSpanId']
        graph[parentSpanId].append(spanId)
        in_degree[spanId] = 0
        if parentSpanId != '-1':
            in_degree[spanId] += 1
    
    queue = deque([span for span in trace1 if in_degree[span['spanId']] == 0])
    
    while queue:
        span = queue.popleft()
        for child in graph[span['spanId']]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(next(s for s in trace1 if s['spanId'] == child))
    
    return 'Yes' if any(in_degree[spanId] > 0 for span in trace1 for spanId in [span['spanId'], span['parentSpanId']]) else 'No'
