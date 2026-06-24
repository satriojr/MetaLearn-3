import os
import json
import google.generativeai as genai
from typing import Optional


class GeminiNLPEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def ask(self, question: str, context: Optional[dict] = None) -> str:
        context = context or {}

        system_prompt = (
            "Kamu adalah MetaLearn AI — asisten pembelajaran adaptif untuk siswa sekolah menengah Indonesia. "
            "Gunakan bahasa Indonesia yang ramah dan mudah dipahami oleh remaja. "
            "Berikan jawaban yang mendidik dengan contoh sederhana jika relevan. "
            "Jika pertanyaan di luar materi pelajaran, arahkan kembali ke topik belajar."
        )

        if context.get("memory"):
            system_prompt += f"\n\n## KONTEKS SISWA\n{context['memory']}"

        if context.get("mission_context"):
            system_prompt += f"\n\n## KONTEKS MATERI\n{context['mission_context']}"

        prompt = f"{system_prompt}\n\nPertanyaan siswa: {question}\n\nJawab dengan jelas dan mendidik:"

        response = self.model.generate_content(prompt)
        return response.text if response.text else "Maaf, saya tidak dapat memproses pertanyaan saat ini."

    def generate_summary(self, session_data: dict, memory: str = "") -> str:
        prompt = (
            "Buat ringkasan sesi belajar dalam bahasa Indonesia dalam format Markdown:\n\n"
            f"Data sesi: {json.dumps(session_data, indent=2)}\n\n"
            f"Memori sebelumnya: {memory}\n\n"
            "Buat ringkasan dengan bagian:\n"
            "- **Aktivitas**: apa yang dipelajari\n"
            "- **Pencapaian**: skor, XP didapat\n"
            "- **Kesulitan**: topik yang masih membingungkan\n"
            "- **Saran**: rekomendasi untuk sesi berikutnya"
        )
        response = self.model.generate_content(prompt)
        return response.text if response.text else "Tidak ada ringkasan tersedia."

    def generate_questions(self, topic: str, difficulty: str, count: int = 5) -> list:
        prompt = (
            f"Buat {count} soal {difficulty} tentang '{topic}' untuk siswa SMA Indonesia. "
            "Setiap soal harus dalam format JSON:\n"
            '{"questions": [{"type": "multiple_choice", "question_text": "...", '
            '"options": [{"label": "A", "text": "..."}, ...], '
            '"correct_answer": "A", "explanation": "..."}, ...]}\n\n'
            "Gunakan bahasa Indonesia. Respond with valid JSON only."
        )

        response = self.model.generate_content(prompt)
        text = response.text if response.text else "[]"

        text = text.replace("```json", "").replace("```", "").strip()
        try:
            data = json.loads(text)
            return data.get("questions", [])
        except json.JSONDecodeError:
            return []

    def generate_learning_path(self, profile: dict) -> dict:
        prompt = (
            "Buat jalur belajar yang dipersonalisasi berdasarkan profil siswa berikut:\n"
            f"{json.dumps(profile, indent=2)}\n\n"
            "Hasilkan dalam format JSON:\n"
            '{"learning_paths": [{"name": "...", "description": "...", '
            '"difficulty_level": "beginner|intermediate|advanced", '
            '"missions": [{"title": "...", "description": "...", '
            '"type": "quiz|interactive", "difficulty": 1-3, '
            '"xp_reward": 50-100, "estimated_minutes": 10-30}]}],\n'
            '"reasoning": "penjelasan singkat mengapa jalur ini dipilih"}\n\n'
            "Gunakan bahasa Indonesia. Respond with valid JSON only."
        )

        response = self.model.generate_content(prompt)
        text = response.text if response.text else "{}"

        text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"learning_paths": [], "reasoning": "Gagal menghasilkan jalur belajar."}
