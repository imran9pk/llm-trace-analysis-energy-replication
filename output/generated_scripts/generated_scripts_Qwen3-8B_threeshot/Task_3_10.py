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
    recursion_stack = set()
    
    def is_cyclic(span_id):
        if span_id in recursion_stack:
            return True
        if span_id in visited:
            return False
        visited.add(span_id)
        recursion_stack.add(span_id)
        parent_span = next((s for s in spans if s['spanId'] == span_id), None)
        if parent_span:
            parent_id = parent_span['parentSpanId']
            if parent_id != -1:
                if is_cyclic(parent_id):
                    return True
        recursion_stack.remove(span_id)
        return False
    
    for span in spans:
        if span['parentSpanId'] != -1:
            if is_cyclic(span['spanId']):
                return "Yes"
    return "No"
