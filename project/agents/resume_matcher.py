from difflib import SequenceMatcher

class MatchAgent:
    def __init__(self):
        pass

    def run(self, resume_data: dict, job_data: dict) -> dict:
        resume_skills = set(resume_data.get("skills", []))
        job_skills = set(job_data.get("required_skills", []))

        matched = resume_skills.intersection(job_skills)
        missing = job_skills - matched

        score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

        return {
            "match_score": score,
            "missing_skills": list(missing),
            "strengths": list(matched),
            "recommendations": (
                "Consider improving skills in: " + ", ".join(missing)
                if missing else "You are a great fit for this role!"
            )
        }

