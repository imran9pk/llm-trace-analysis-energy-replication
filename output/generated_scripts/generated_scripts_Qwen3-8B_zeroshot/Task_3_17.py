"""
Auto-generated task-level solver.

Task ID: Task_3_17
Task Type: 6_Ranking
Task Description: Identify which table is accessed most frequently in a given trace.
Question Template: Which table is accessed most frequently in the Input Trace?
"""

def solution(trace1):
    from collections import defaultdict

    table_access_count = defaultdict(int)
    span_tree = {}

    for span in trace1:
        span_id = span['spanId']
        parent_span_id = span['parentSpanId']
        name = span['name']
        kind = span['kind']

        span_tree[span_id] = {
            'parent': parent_span_id,
            'name': name,
            'kind': kind
        }

    def traverse(span_id):
        span = span_tree[span_id]
        if span['kind'] == 'SERVER':
            if '/' in span['name']:
                table_name = span['name'].split('/')[-1]
                if table_name in ['table1', 'table2', 'table3']:
                    table_access_count[table_name] += 1
        if span['parent'] != -1:
            traverse(span['parent'])

    for span_id in span_tree:
        traverse(span_id)

    max_count = max(table_access_count.values()) if table_access_count else 0
    result = [table for table, count in table_access_count.items() if count == max_count]
    return result
