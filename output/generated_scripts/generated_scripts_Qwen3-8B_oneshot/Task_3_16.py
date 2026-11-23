"""
Auto-generated task-level solver.

Task ID: Task_3_16
Task Type: 6_Ranking
Task Description: Identify which type of SQL statement is executed most frequently in a given trace.
Question Template: Which type of SQL statement is executed most frequently in the Input Trace?
"""

def solution(trace1):
    sql_counts = {'INSERT': 0, 'DELETE': 0, 'UPDATE': 0, 'SELECT': 0}
    for span in trace1:
        if 'db.operation' in span:
            operation = span['db.operation'].upper()
            if operation in sql_counts:
                sql_counts[operation] += 1
    max_count = max(sql_counts.values())
    return [stmt for stmt, count in sql_counts.items() if count == max_count]
