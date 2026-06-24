import json
import os
from typing import Optional

import google.generativeai as genai


class AdaptivePathwayEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_pathway(
        self,
        interests: list[str],
        learning_style: str,
        mastery_scores: Optional[dict] = None,
        completed_missions: Optional[list] = None,
    ) -> dict:
        mastery_scores = mastery_scores or {}
        completed_missions = completed_missions or []

        prompt = (
            "Buat jalur belajar adaptif berdasarkan profil siswa:\n\n"
            f"Minat: {', '.join(interests)}\n"
            f"Gaya belajar: {learning_style}\n"
            f"Skor penguasaan: {json.dumps(mastery_scores)}\n"
            f"Misi terselesaikan: {json.dumps(completed_missions)}\n\n"
            "Hasilkan dalam format JSON:\n"
            '{"pathways": [{"name": "...", "description": "...", '
            '"difficulty": "beginner|intermediate|advanced", '
            '"reason": "mengapa ini direkomendasikan", '
            '"missions": [{"title": "...", "difficulty": 1-3, '
            '"xp": 50-100, "estimated_minutes": 10-30}]}],\n'
            '"overall_reasoning": "penjelasan strategi belajar"}\n\n'
            "Gunakan bahasa Indonesia. Respond with valid JSON only."
        )

        response = self.model.generate_content(prompt)
        text = response.text if response.text else "{}"

        text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {
                "pathways": [],
                "overall_reasoning": "Gagal menghasilkan jalur belajar.",
            }

    def generate_remedial_mission(self, weak_topics: list[str], learning_style: str) -> dict:
        prompt = (
            f"Siswa kesulitan pada topik: {', '.join(weak_topics)}\n"
            f"Gaya belajar: {learning_style}\n\n"
            "Buat misi remedial yang membantu siswa menguasai topik tersebut. "
            "Hasilkan JSON:\n"
            '{"remedial_missions": [{"title": "...", "description": "...", '
            '"type": "interactive|quiz", "difficulty": 1, '
            '"tips": ["tip1", "tip2"], "xp_reward": 60, '
            '"estimated_minutes": 15}]}\n\n'
            "Gunakan bahasa Indonesia. Respond with valid JSON only."
        )

        response = self.model.generate_content(prompt)
        text = response.text if response.text else "{}"

        text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"remedial_missions": []}
