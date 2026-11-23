"""
Auto-generated task-level solver.

Task ID: Task_1_6
Task Type: 2_Ranking
Task Description: Identify the child span with the longest response time of a given span.
Question Template: Which child span of span '{key_component}' has the longest response time in the Input Trace?
"""

def solution(trace1, key_component):
    def get_child_span_with_longest_response_time(trace, parent_span_id):
        max_duration = 0
        longest_span_id = None

        for span in trace:
            if span['parentSpanId'] == parent_span_id:
                duration = int(span['durationTimeUnixNano'])
                if duration > max_duration:
                    max_duration = duration
                    longest_span_id = span['spanId']

        return longest_span_id

    return get_child_span_with_longest_response_time(trace1, key_component)
