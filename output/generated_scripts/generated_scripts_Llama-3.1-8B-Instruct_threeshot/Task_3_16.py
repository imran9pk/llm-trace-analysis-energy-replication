"""
Auto-generated task-level solver.

Task ID: Task_3_16
Task Type: 6_Ranking
Task Description: Identify which type of SQL statement is executed most frequently in a given trace.
Question Template: Which type of SQL statement is executed most frequently in the Input Trace?
"""

def solution(trace1):
    sql_statements = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
    sql_counts = {statement: 0 for statement in sql_statements}
    
    for span in trace1:
        if 'db.operation' in span:
            sql_counts[span['db.operation']] += 1
    
    max_count = max(sql_counts.values())
    most_frequent_sql = [statement for statement, count in sql_counts.items() if count == max_count]
    
    return most_frequent_sql
