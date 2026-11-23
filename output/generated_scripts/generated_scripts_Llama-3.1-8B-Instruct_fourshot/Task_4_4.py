"""
Auto-generated task-level solver.

Task ID: Task_4_4
Task Type: 8_Comparison
Task Description: Identify the trace with a greater depth between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater depth?
"""

from collections import defaultdict, deque

def solution(trace1, trace2):
    def get_depth(trace):
        graph = defaultdict(list)
        for span in trace:
            if span['parentSpanId'] != '-1':
                graph[span['spanId']].append(span['parentSpanId'])
        
        visited = set()
        max_depth = 0
        queue = deque([(span['spanId'], 1) for span in trace if span['spanId'] == '-1'])
        
        while queue:
            span_id, depth = queue.popleft()
            if span_id not in visited:
                visited.add(span_id)
                max_depth = max(max_depth, depth)
                for parent in graph[span_id]:
                    queue.append((parent, depth + 1))
        
        return max_depth
    
    return 'Same' if get_depth(trace1) == get_depth(trace2) else '6rS6URzYbDEq4IP888ZOeA==' if get_depth(trace1) > get_depth(trace2) else 'XQp9YPBu5/8rhsdNUtYmoQ=='
