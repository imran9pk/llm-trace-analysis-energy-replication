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
            if span['http.status_code'] != '200':
                abnormal_spans.append(span['name'])
        return abnormal_spans

    def get_abnormal_spans_from_trace(trace):
        abnormal_spans = []
        for span in trace:
            if span['http.status_code'] != '200':
                abnormal_spans.append(span['name'])
            if 'parentSpanId' in span and span['parentSpanId'] != '-1':
                abnormal_spans.extend(get_abnormal_spans_from_trace([s for s in trace if s['spanId'] == span['parentSpanId']]))
        return abnormal_spans

    return get_abnormal_spans_from_trace(trace1)
