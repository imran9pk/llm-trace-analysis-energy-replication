"""
Auto-generated task-level solver.

Task ID: Task_3_16
Task Type: 6_Ranking
Task Description: Identify which type of SQL statement is executed most frequently in a given trace.
Question Template: Which type of SQL statement is executed most frequently in the Input Trace?
"""

def solution(trace1):
    sql_types = {'INSERT': 0, 'DELETE': 0, 'UPDATE': 0, 'SELECT': 0}
    for span in trace1:
        if 'sql' in span.get('attributes', {}) and span['attributes']['sql'] in sql_types:
            sql_types[span['attributes']['sql']] += 1
    max_count = max(sql_types.values())
    return [sql for sql, count in sql_types.items() if count == max_count]
