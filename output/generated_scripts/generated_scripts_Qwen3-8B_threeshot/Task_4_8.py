"""
Auto-generated task-level solver.

Task ID: Task_4_8
Task Type: 8_Comparison
Task Description: Determine whether the two given traces involve the same set of operations.
Question Template: Are the sets of operations involved in the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    def extract_operations(trace):
        operations = set()
        for span in trace:
            if 'db.operation' in span:
                operations.add(span['db.operation'])
            elif 'http.route' in span:
                operations.add(span['http.route'])
            elif 'name' in span:
                operations.add(span['name'])
        return operations
    
    operations1 = extract_operations(trace1)
    operations2 = extract_operations(trace2)
    
    return 'Yes' if operations1 == operations2 else 'No'
