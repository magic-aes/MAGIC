from .base import BasePrompts

class GREGeneralGraderPrompts(BasePrompts):
    system_prompt = """
You are an expert professional grader who scores student essays tagged <student_essay> based on a rubric. 
Please provide a numerical score for the provided essay according to the specified rubric.

- Provide an appropriate holistic score.
- You will carefully read the rubric (<rubric>), prompt (<essay_prompt>) and student essay (<student_essay>), as many times as needed.
- You will provide a detailed explanation of your reasoning for the score using the rubric as an examiner's comment.
- The length of the essay matters, a well developed essay should have at least 3-4 well written paragraphs.
- A low score isn't harmful to the student. Rather, an accurate match to the rubric will help the student improve their score in future essays.

The rubric or rubrics for this essay is as follows:
<rubric>
{rubric}
</rubric>

The prompt is as follows:
<essay_prompt>
{prompt}
</essay_prompt>

Review the given rubric and prompt carefully and score the <student_essay>.
Provide a numerical score between {min_score} and {max_score} by using the provided rubric's guidance.
Remember, a low score isn't harmful to the student. Rather, an accurate match to the rubric will help the student improve their score in future essays.

{output_format}
"""
    

    @classmethod
    def dump_prompts(cls) -> dict:
        return {
            "system_prompt": cls.system_prompt,
            "input_prompt": cls.input_prompt,
        }
    
    @classmethod
    def format_prompt_inference(cls, grading_instruction: dict, current_rubric: str) -> str:
        essay_text = grading_instruction["essay_text"]

        system_prompt_formatted = cls.system_prompt.format(
            prompt=grading_instruction["prompt"],
            rubric=current_rubric,
            output_format=cls.output_format,
            min_score=0,
            max_score=6
        )

        input_prompt_formatted = cls.input_prompt.format(
            essay_text=essay_text
        )
        return cls.alpaca_prompt.format(system_prompt_formatted, input_prompt_formatted, "")