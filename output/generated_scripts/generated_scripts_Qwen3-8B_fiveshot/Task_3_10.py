"""
Auto-generated task-level solver.

Task ID: Task_3_10
Task Type: 5_Existence
Task Description: Determine whether a cyclic call issue exists in a given trace.
Question Template: Is there a cyclic call issue in the Input Trace?
"""

def solution(trace1):
    spans = trace1
    service_map = {}
    visited = set()
    in_stack = set()
    
    def dfs(span_id):
        span = next((s for s in spans if s['spanId'] == span_id), None)
        if not span:
            return False
        if span_id in visited:
            return False
        if span_id in in_stack:
            return True
        in_stack.add(span_id)
        parent_id = span['parentSpanId']
        if parent_id != -1:
            if dfs(parent_id):
                return True
        visited.add(span_id)
        in_stack.remove(span_id)
        return False
    
    for span in spans:
        if span['parentSpanId'] != -1:
            if dfs(span['spanId']):
                return 'Yes'
    return 'No'
