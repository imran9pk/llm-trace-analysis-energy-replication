"""
Auto-generated task-level solver.

Task ID: Task_3_21
Task Type: 6_Entity
Task Description: Identify the spans with abnormal response codes in a given trace.
Question Template: Which spans have abnormal response codes in the Input Trace?
"""

def solution(trace1):
    def get_abnormal_spans(trace):
        abnormal_spans = []
        for span in trace:
            if span['http.status_code'] != '200':
                abnormal_spans.append(span['spanId'])
        return abnormal_spans

    def get_span_ids(trace):
        span_ids = set()
        for span in trace:
            span_ids.add(span['spanId'])
            if span['parentSpanId'] != '-1':
                span_ids.add(span['parentSpanId'])
        return span_ids

    abnormal_spans = get_abnormal_spans(trace1)
    span_ids = get_span_ids(trace1)
    return list(span_ids - set(abnormal_spans))
