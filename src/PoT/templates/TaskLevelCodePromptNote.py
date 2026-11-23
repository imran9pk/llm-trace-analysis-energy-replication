# templates/TaskLevelCodePromptNote.py

"""
Task-level code prompt notes.

These notes are used when generating one reusable solver script per task type
from TaskInfo.json. Unlike the original instance-level CodePromptTemplate.py,
these notes use parameterized function signatures whenever the task question
contains runtime key components such as {key_component}, {key_component_1},
or {key_component_2}.
"""


task_level_note_single_trace_one_key = """
## Function Specification
Write a general-purpose Python function with this exact signature:

```python
def solution(trace1, key_component):
    # function body
    return answer
```

- `trace1` is one input trace.
- `key_component` is extracted from the concrete question at runtime.
"""


task_level_note_single_trace_two_keys = """
## Function Specification
Write a general-purpose Python function with this exact signature:

```python
def solution(trace1, key_component_1, key_component_2):
    # function body
    return answer
```

- `trace1` is one input trace.
- `key_component_1` and `key_component_2` are extracted from the concrete question at runtime.
"""


task_level_note_single_trace_no_key = """
## Function Specification
Write a general-purpose Python function with this exact signature:

```python
def solution(trace1):
    # function body
    return answer
```

- `trace1` is one input trace.
"""


task_level_note_two_traces = """
## Function Specification
Write a general-purpose Python function with this exact signature:

```python
def solution(trace1, trace2):
    # function body
    return answer
```

- `trace1` and `trace2` are the two input traces.
"""

common_task_level_requirements = """
## Requirements
- Do not hardcode span IDs, service names, host names, trace IDs, routes, timestamps, or example-specific values.
- Return only the exact answer value: a number, string, list, or empty list [].
- Do not return span dictionaries, trace labels, or any surrounding structure unless explicitly asked.
- Time-related fields such as `startTimeUnixNano`, `endTimeUnixNano`, and `durationTimeUnixNano` are strings and must be converted to integers before arithmetic.
- Do not include explanations, reasoning, or any text outside the ```python ... ``` code block in your response.
"""

# Example template for few-shot code generation.
code_example_template = \
"""
## Example {example_id}
- Question
{question}
- Input Trace(s)
{input_traces}
- Answer
{answer}
"""