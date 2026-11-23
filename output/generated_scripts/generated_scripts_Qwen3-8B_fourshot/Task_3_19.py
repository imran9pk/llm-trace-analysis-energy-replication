"""
Auto-generated task-level solver.

Task ID: Task_3_19
Task Type: 6_Ranking
Task Description: Identify the database operation with the longest execution time in a given trace.
Question Template: Which database operation has the longest execution time in the Input Trace?
"""

def solution(trace1):
    max_duration = 0
    max_ops = []
    for span in trace1:
        if 'db.operation' in span:
            duration = int(span['durationTimeUnixNano'])
            if duration > max_duration:
                max_duration = duration
                max_ops = [span['db.operation']]
            elif duration == max_duration:
                max_ops.append(span['db.operation'])
    return max_ops
