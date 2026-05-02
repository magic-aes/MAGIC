from .base import BasePrompts
from pydantic import BaseModel

class RubricJudgePrompts(BasePrompts):
    system_prompt = """
You are an expert professional grader who specializes in evaluating feedback from expert graders.
You will be given two feedbacks for an essay crafted by two expert graders. 
You will choose the better feedback (<feedback_1> or <feedback_2>) for each of the criteria specified in <criteria>.

<criteria>
- C1: Which feedback is more relevant to the essay content?
- C2: Which feedback is better at highlighting weakness?
- C3: Which feedback is better at highlighting strengths?
- C4: Which feedback is more specific and actionable?
- C5: Which feedback is overall more helpful for a student?
</criteria>

The rubric for the essay is as follows:
<rubric>
{rubric}
</rubric>

The two feedbacks are as follows:
<feedback_1>
{feedback_1}
</feedback_1>

<feedback_2>
{feedback_2}
</feedback_2>

The prompt is as follows:
<essay_prompt>
{prompt}
</essay_prompt>

The student essay is as follows:
<student_essay>
{student_essay}
</student_essay>

Provide a number (1 or 2) representing the feedback that you choose for each of the criteria.

{output_format}
"""
    output_format = """
Your output should be a JSON in the following format:
{
    "c1": (1 or 2),
    "c2": (1 or 2),
    "c3": (1 or 2),
    "c4": (1 or 2),
    "c5": (1 or 2)
}
"""
    class ResponseModel(BaseModel):
        c1: int
        c2: int
        c3: int
        c4: int
        c5: int
        summary: list[str]

    @classmethod
    def dump_prompts(cls) -> dict:
        return {
            "system_prompt": cls.system_prompt,
            "output_format": cls.output_format,
        }
    
    @classmethod
    def format_prompt_judge(cls, feedback_1: str, feedback_2: str, student_essay: str, prompt: str) -> str:
        return cls.system_prompt.format(
            feedback_1=feedback_1,
            feedback_2=feedback_2,
            student_essay=student_essay,
            rubric=cls.rubric,
            prompt=prompt,
            output_format=cls.output_format,
        )
