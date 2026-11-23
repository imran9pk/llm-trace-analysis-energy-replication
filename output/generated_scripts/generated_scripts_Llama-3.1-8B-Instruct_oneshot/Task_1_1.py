"""
Auto-generated task-level solver.

Task ID: Task_1_1
Task Type: 1_Entity
Task Description: Identify which services are called by a given service.
Question Template: Which services are called by the service '{key_component}' in the Input Trace?
"""

def solution(trace1, key_component):
    graph = {}
    for span in trace1:
        if span['parentSpanId'] not in graph:
            graph[span['parentSpanId']] = []
        graph[span['parentSpanId']].append(span['service.name'])
        if span['spanId'] not in graph:
            graph[span['spanId']] = []
    for span in trace1:
        if span['spanId'] not in graph:
            graph[span['spanId']] = []
    callees = set()
    for span in trace1:
        if span['service.name'] == key_component:
            if span['parentSpanId'] != '-1':
                callees.add(trace1[int(span['parentSpanId']) - 1]['service.name'])
    return list(callees)
