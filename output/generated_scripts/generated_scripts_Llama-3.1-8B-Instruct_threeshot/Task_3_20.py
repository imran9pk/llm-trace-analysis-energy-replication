"""
Auto-generated task-level solver.

Task ID: Task_3_20
Task Type: 6_Entity
Task Description: Identify the operations with abnormal response codes in a given trace.
Question Template: Which operations have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    def get_abnormal_spans(trace):
        abnormal_spans = []
        for span in trace:
            if 'http.status_code' in span and span['http.status_code'] != '200':
                abnormal_spans.append(span['name'])
            elif 'db.operation' in span and span['db.operation'] in ['INSERT', 'UPDATE', 'DELETE']:
                abnormal_spans.append(span['name'])
        return abnormal_spans

    return get_abnormal_spans(trace1)
