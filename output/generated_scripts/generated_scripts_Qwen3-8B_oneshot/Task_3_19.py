"""
Auto-generated task-level solver.

Task ID: Task_3_19
Task Type: 6_Ranking
Task Description: Identify the database operation with the longest execution time in a given trace.
Question Template: Which database operation has the longest execution time in the Input Trace?
"""

def solution(trace1):
    max_duration = 0
    longest_ops = []
    for span in trace1:
        if 'db.system' in span and 'db.operation' in span:
            duration = int(span['durationTimeUnixNano'])
            if duration > max_duration:
                max_duration = duration
                longest_ops = [span['db.operation']]
            elif duration == max_duration:
                longest_ops.append(span['db.operation'])
    return longest_ops
