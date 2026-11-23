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

    def get_span_id(trace):
        span_id = set()
        for span in trace:
            span_id.add(span['spanId'])
        return span_id

    def get_parent_span_id(trace):
        parent_span_id = set()
        for span in trace:
            parent_span_id.add(span['parentSpanId'])
        return parent_span_id

    def get_all_spans(trace):
        all_spans = set()
        for span in trace:
            all_spans.add(span['spanId'])
        return all_spans

    def get_abnormal_spans_in_tree(trace):
        abnormal_spans = set()
        for span in trace:
            if span['spanId'] in get_abnormal_spans(trace):
                abnormal_spans.add(span['spanId'])
            elif span['parentSpanId'] != '-1' and span['spanId'] in get_all_spans(trace):
                abnormal_spans.update(get_abnormal_spans_in_tree([s for s in trace if s['parentSpanId'] == span['spanId']]))
        return abnormal_spans

    return list(get_abnormal_spans_in_tree(trace1))
