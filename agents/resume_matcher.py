from difflib import SequenceMatcher

class MatchAgent:
    def __init__(self, threshold: float = 0.455555555555556):
        self.threshold = threshold

    def _is_similar(self, skill1: str, skill2: str) -> bool:
        return SequenceMatcher(None, skill1.lower(), skill2.lower()).ratio() >= self.threshold

    def run(self, resume_data: dict, job_data: dict) -> dict:
        resume_skills = set(resume_data.get("skills", []))
        job_skills = set(job_data.get("required_skills", []))

        matched = set()
        unmatched = set(job_skills)

        for job_skill in job_skills:
            for resume_skill in resume_skills:
                if self._is_similar(job_skill, resume_skill):
                    matched.add(job_skill)
                    unmatched.discard(job_skill)
                    break

        score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

        return {
            "match_score": score,
            "missing_skills": list(unmatched),
            "strengths": list(matched),
            "recommendations": (
                "Consider improving skills in: " + ", ".join(unmatched)
                if unmatched else "You are a great fit for this role!"
            )
        }

