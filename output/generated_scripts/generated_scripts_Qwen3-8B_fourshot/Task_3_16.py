"""
Auto-generated task-level solver.

Task ID: Task_3_16
Task Type: 6_Ranking
Task Description: Identify which type of SQL statement is executed most frequently in a given trace.
Question Template: Which type of SQL statement is executed most frequently in the Input Trace?
"""

def solution(trace1):
    sql_counts = {'SELECT': 0, 'INSERT': 0, 'UPDATE': 0, 'DELETE': 0}
    for span in trace1:
        if 'db.operation' in span:
            operation = span['db.operation'].upper()
            if operation in sql_counts:
                sql_counts[operation] += 1
    max_count = max(sql_counts.values())
    result = [k for k, v in sql_counts.items() if v == max_count]
    return result
