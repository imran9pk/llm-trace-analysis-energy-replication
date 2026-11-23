# system prompt
system_prompt_with_step = \
"""
You are an advanced AI specialized in trace analysis problems. Provide the solution without writing or executing any code. The solution consists of the explicit reasoning path and the final answer, where the final answer is presented within <<<>>>.
"""

system_prompt_without_step = \
"""
You are an advanced AI specialized in trace analysis problems. Provide the solution without writing or executing any code. The solution includes only the final answer, which is presented within <<<>>>.
"""

system_prompt_with_code = \
"""
You are an advanced AI specialized in trace analysis problems. Provide the solution by writing code. The solution includes only a callable Python function that returns the answer. Please provide the code directly without any reasoning process.
"""


# user instruction
instruction_template = \
"""
Below is an instruction that describes a trace analysis task. Write a response that appropriately completes the request.

## Domain Knowledge
- Trace Definition:
All traces in this task follow the {specification_name} specification.
- Trace Description:
{trace_format}

## Instruction
{task_description}
{task_definition}
Question: {question} Let us answer this question step by step to make it correct.
Input Trace(s): {trace}

## Response
"""

instruction_template_with_input_traces = \
"""
Below is an instruction that describes a trace analysis task. Write a response that appropriately completes the request.

## Domain Knowledge
- Trace Definition:
All traces in this task follow the {specification_name} specification.
- Trace Description:
{trace_format}

## Instruction
{task_description}
{task_definition}
Question: {question} Let us answer this question step by step to make it correct.
Input Trace(s): {trace}
"""

instruction_template_without_input_traces = \
"""
Below is an instruction that describes a trace analysis task. Write a response that appropriately completes the request.

## Domain Knowledge
- Trace Definition:
All traces in this task follow the {specification_name} specification.
- Trace Description:
{trace_format}

## Instruction
{task_description}
{task_definition}
Question: {question}
"""


# CoT example
cot_example_template = \
"""
## Example {example_id}
- Question
{question}
- Input Trace(s)
{input_traces}
- Response
{response}
"""