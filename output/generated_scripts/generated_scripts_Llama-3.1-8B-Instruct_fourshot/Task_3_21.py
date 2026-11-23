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
        return span_ids

    def get_parent_span_ids(trace):
        parent_span_ids = set()
        for span in trace:
            parent_span_ids.add(span['parentSpanId'])
        return parent_span_ids

    def get_all_spans(trace):
        all_spans = set()
        for span in trace:
            all_spans.add(span['spanId'])
        return all_spans

    def get_abnormal_spans_in_tree(trace):
        abnormal_spans = set()
        span_ids = get_span_ids(trace)
        parent_span_ids = get_parent_span_ids(trace)
        all_spans = get_all_spans(trace)
        abnormal_spans_in_tree = set()
        for span_id in all_spans:
            if span_id not in parent_span_ids and span_id in span_ids:
                abnormal_spans_in_tree.update(get_abnormal_spans(trace))
        return list(abnormal_spans_in_tree)

    return get_abnormal_spans_in_tree(trace1)
