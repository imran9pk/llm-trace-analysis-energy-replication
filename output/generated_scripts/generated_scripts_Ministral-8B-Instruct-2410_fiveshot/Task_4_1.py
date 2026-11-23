"""
Auto-generated task-level solver.

Task ID: Task_4_1
Task Type: 7_Comparison
Task Description: Determine whether the response codes of two given traces are the same.
Question Template: Are the response codes of the Input Trace '{key_component_1}' and the Input Trace '{key_component_2}' the same?
"""

def solution(trace1, trace2):
    # Extract the response codes from the traces
    response_codes1 = [span['http.status_code'] for span in trace1 if 'http.status_code' in span]
    response_codes2 = [span['http.status_code'] for span in trace2 if 'http.status_code' in span]

    # Convert the response codes to integers
    response_codes1 = [int(code) for code in response_codes1]
    response_codes2 = [int(code) for code in response_codes2]

    # Compare the response codes
    if response_codes1 == response_codes2:
        return 'Yes'
    else:
        return 'No'
