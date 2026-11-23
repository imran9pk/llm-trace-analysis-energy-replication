"""
Auto-generated task-level solver.

Task ID: Task_3_19
Task Type: 6_Ranking
Task Description: Identify the database operation with the longest execution time in a given trace.
Question Template: Which database operation has the longest execution time in the Input Trace?
"""

def solution(trace1):
    max_duration = 0
    longest_spans = []
    for span in trace1:
        duration = int(span['durationTimeUnixNano'])
        if 'db.operation' in span and duration > max_duration:
            max_duration = duration
            longest_spans = [span]
        elif 'db.operation' in span and duration == max_duration:
            longest_spans.append(span)
    return longest_spans
