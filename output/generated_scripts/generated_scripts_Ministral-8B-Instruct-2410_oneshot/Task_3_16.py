"""
Auto-generated task-level solver.

Task ID: Task_3_16
Task Type: 6_Ranking
Task Description: Identify which type of SQL statement is executed most frequently in a given trace.
Question Template: Which type of SQL statement is executed most frequently in the Input Trace?
"""

def solution(trace1):
    from collections import Counter

    sql_statements = [span['name'] for span in trace1 if 'db.operation' in span]
    sql_counts = Counter(sql_statements)
    max_count = max(sql_counts.values())
    most_frequent_sqls = [sql for sql, count in sql_counts.items() if count == max_count]

    return most_frequent_sqls
