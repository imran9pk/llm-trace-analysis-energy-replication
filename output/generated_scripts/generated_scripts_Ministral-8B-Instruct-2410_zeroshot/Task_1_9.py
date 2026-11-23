"""
Auto-generated task-level solver.

Task ID: Task_1_9
Task Type: 2_Computation
Task Description: Identify the local execution time of a given span.
Question Template: What is the local execution time of span '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    def parse_time(time_str):
        return int(time_str)

    def find_span(span_list, key_component):
        for span in span_list:
            if span['name'] == key_component:
                return span
            if 'children' in span:
                child_span = find_span(span['children'], key_component)
                if child_span:
                    return child_span
        return None

    def calculate_local_execution_time(span):
        if span['kind'] == 'PRODUCER':
            return parse_time(span['durationTimeUnixNano'])
        else:
            total_child_duration = sum(parse_time(child['durationTimeUnixNano']) for child in span.get('children', []))
            return parse_time(span['durationTimeUnixNano']) - total_child_duration

    span = find_span(trace1, key_component)
    if span:
        return calculate_local_execution_time(span)
    return 0
