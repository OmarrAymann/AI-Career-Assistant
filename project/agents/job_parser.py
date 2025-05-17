import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json5
import regex as re
from llm_interface import ask_llm

class JobParserAgent:
    def __init__(self):
        pass

    def run(self, job_description: str) -> dict:
        prompt = f"""
You are an expert job analysis assistant. Your task is to extract structured information from a job description. Focus on understanding the *skills*, *experience*, and *tools* required, as well as identifying *important keywords* that describe the role.

Analyze the job description below and return a **well-formatted JSON object** with the following keys:
- **required_skills**: A list of core technical and non-technical skills explicitly required for the role.
- **required_experience**: A brief sentence or phrase describing the minimum experience required (e.g., "3+ years in software development").
- **preferred_tools_or_technologies**: A list of tools, frameworks, or technologies mentioned as preferred or nice-to-have.
- **keywords**: A list of important role-specific keywords or phrases that summarize the job responsibilities or focus areas.

Only return a valid JSON object. Do not include any explanation, markdown, or extra text.

Job description:
\"\"\"{job_description}\"\"\"

Return only a valid JSON object with keys:
- required_skills
- required_experience
- preferred_tools_or_technologies
- keywords
"""
        raw_result = ask_llm(prompt)

        # 🛠️ Extract the first JSON block using robust regex
        for attempt in range(2):
            try:
                json_match = re.search(r'\{(?:[^{}]|\n|\\{|\\})*\}', raw_result)
                if not json_match:
                    raise ValueError("No JSON block found.")
                json_str = json_match.group(0)
                parsed = json5.loads(json_str)
                return parsed
            except Exception as e:
                if attempt == 1:
                    raise e
                raw_result = ask_llm("Return only valid JSON:\n" + raw_result)
