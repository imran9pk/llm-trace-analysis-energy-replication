"""
Auto-generated task-level solver.

Task ID: Task_4_10
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of service instance call pairs.
Question Template: Are the sets of service instance call pairs involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    # Convert the traces to a set of tuples (spanId, parentSpanId, name, kind, startTimeUnixNano, endTimeUnixNano, durationTimeUnixNano, service.name, host.name, http.route, http.status_code, db.operation, db.sql.table, db.name, db.system)
    trace1_set = {(span['spanId'], span['parentSpanId'], span['name'], span['kind'], int(span['startTimeUnixNano']), int(span['endTimeUnixNano']), int(span['durationTimeUnixNano']), span['service.name'], span['host.name'], span['http.route'], span['http.status_code'], span['db.operation'], span['db.sql.table'], span['db.name'], span['db.system']) for span in trace1}
    trace2_set = {(span['spanId'], span['parentSpanId'], span['name'], span['kind'], int(span['startTimeUnixNano']), int(span['endTimeUnixNano']), int(span['durationTimeUnixNano']), span['service.name'], span['host.name'], span['http.route'], span['http.status_code'], span['db.operation'], span['db.sql.table'], span['db.name'], span['db.system']) for span in trace2}

    # Check if the sets are equal
    return 'Yes' if trace1_set == trace2_set else 'No'
