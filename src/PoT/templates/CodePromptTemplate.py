codeprompt_template = \
"""
Your task is to write an executable Python code snippet to solve the following question.

## Domain Knowledge
- Trace Definition:
All traces in this task follow the {specification_name} specification.
- Trace Description:
{trace_format}

## Instruction
{task_description}
{task_definition}
Question: {question}

## Note
- You should generate an executable Python code snippet and print the answer to the question. 
- The input is a trace or trace pair represented in the format specified by Trace Description.
- The output may be a number, a string, or a list, which can be empty (i.e., []). The output is presented within <<<>>>.
"""

code_prompt_note = \
"""
## Note: You need to write a Python function according to the following specifications:
- The function name is `solution`.
- The input of the function is the trace description in Input Trace(s). If there is only one trace, the input parameter is `trace1`. If there are two traces, the input parameters are `trace1` and `trace2`.
- The output of the function is the answer to the question, which may be a number, a string, a list, or empty (i.e., []). Keep answers concise and include only necessary information. For example, if the trace ID needs to be output, output the trace ID directly without any extra explanation.
- No need to write the function call statement.
- Time-related problems require converting `startTimeUnixNano`, `endTimeUnixNano`, etc., to integers before performing calculations.
- If there is only one trace, the function template is:
```python
def solution(trace1):
    # function body
    return answer
```
- If there are two traces, the function template is:
```python
def solution(trace1, trace2):
    # function body
    return answer
```
"""


function_call_template_one_trace = \
"""
trace1 = {trace1}
answer = solution(trace1)
print('<<<' + str(answer) + '>>>')
"""


function_call_template_two_traces = \
"""
trace1 = {trace1}
trace2 = {trace2}
answer = solution(trace1, trace2)
print('<<<' + str(answer) + '>>>')
"""