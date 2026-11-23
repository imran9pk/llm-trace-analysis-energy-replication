"""
Auto-generated task-level solver.

Task ID: Task_3_16
Task Type: 6_Ranking
Task Description: Identify which type of SQL statement is executed most frequently in a given trace.
Question Template: Which type of SQL statement is executed most frequently in the Input Trace?
"""

def solution(trace1):
    sql_types = {}
    for span in trace1:
        if 'db.operation' in span:
            sql_types[span['db.operation']] = sql_types.get(span['db.operation'], 0) + 1
    max_count = max(sql_types.values())
    return [k for k, v in sql_types.items() if v == max_count]
