"""
Auto-generated task-level solver.

Task ID: Task_3_9
Task Type: 5_Computation
Task Description: Identify the depth of a given trace.
Question Template: What is the depth of the Input Trace?
"""

def solution(trace1):
    def dfs(span):
        if span['parentSpanId'] == -1:
            return 1
        for s in trace1:
            if s['spanId'] == span['parentSpanId']:
                return 1 + dfs(s)
    
    return max(dfs(span) for span in trace1)
