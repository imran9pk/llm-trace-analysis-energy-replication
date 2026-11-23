"""
Auto-generated task-level solver.

Task ID: Task_4_3
Task Type: 8_Comparison
Task Description: Identify the trace with a greater number of spans between two given traces.
Question Template: Which trace, the Input Trace '{key_component_1}' or the Input Trace '{key_component_2}', has a greater number of spans?
"""

def solution(trace1, trace2):
    def count_spans(trace):
        root = {}
        for span in trace:
            span_id = span['spanId']
            parent_span_id = span['parentSpanId']
            if parent_span_id == -1:
                root[span_id] = {'children': [], 'count': 1}
            else:
                if parent_span_id not in root:
                    root[parent_span_id] = {'children': [], 'count': 0}
                root[parent_span_id]['children'].append(span_id)
                root[parent_span_id]['count'] += 1
        def dfs(node):
            count = node['count']
            for child in node['children']:
                count += dfs(root[child])
            return count
        return dfs(root[0])

    return 'Trace 1' if count_spans(trace1) > count_spans(trace2) else 'Trace 2' if count_spans(trace2) > count_spans(trace1) else 'Same'
