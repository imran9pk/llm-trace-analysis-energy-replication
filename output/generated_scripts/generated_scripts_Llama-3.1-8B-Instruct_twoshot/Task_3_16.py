"""
Auto-generated task-level solver.

Task ID: Task_3_16
Task Type: 6_Ranking
Task Description: Identify which type of SQL statement is executed most frequently in a given trace.
Question Template: Which type of SQL statement is executed most frequently in the Input Trace?
"""

def solution(trace1):
    sql_types = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
    sql_count = {sql_type: 0 for sql_type in sql_types}
    
    for span in trace1:
        if 'db.operation' in span:
            sql_type = span['db.operation']
            if sql_type in sql_types:
                sql_count[sql_type] += 1
    
    max_count = max(sql_count.values())
    most_frequent_sql = [sql_type for sql_type, count in sql_count.items() if count == max_count]
    
    return most_frequent_sql
