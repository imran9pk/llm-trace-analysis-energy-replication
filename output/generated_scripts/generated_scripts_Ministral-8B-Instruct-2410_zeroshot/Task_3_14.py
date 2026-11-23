"""
Auto-generated task-level solver.

Task ID: Task_3_14
Task Type: 6_Ranking
Task Description: Identify which operation is executed most frequently in a given trace.
Question Template: Which operation is executed most frequently in the Input Trace?
"""

def solution(trace1):
    from collections import Counter

    # Convert durationTimeUnixNano to integers
    for span in trace1:
        span['durationTimeUnixNano'] = int(span['durationTimeUnixNano'])

    # Count the occurrences of each operation name
    operation_counts = Counter(span['name'] for span in trace1)

    # Find the maximum count
    max_count = max(operation_counts.values())

    # Get all operations with the maximum count
    most_frequent_operations = [name for name, count in operation_counts.items() if count == max_count]

    return most_frequent_operations
