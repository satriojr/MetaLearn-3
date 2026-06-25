import os
import uuid
import time

from engines.gemini import get_gemini_model

MAX_SESSIONS = 100
SESSION_TTL = 3600


class ChatbotEngine:
    def __init__(self):
        self.model = get_gemini_model()
        self.gemini_available = self.model is not None
        self.sessions: dict[str, list[dict]] = {}
        self.session_times: dict[str, float] = {}

    def _evict_stale_sessions(self):
        now = time.time()
        stale = [sid for sid, t in self.session_times.items() if now - t > SESSION_TTL]
        for sid in stale:
            self.sessions.pop(sid, None)
            self.session_times.pop(sid, None)
        if len(self.sessions) > MAX_SESSIONS:
            sorted_by_time = sorted(self.session_times.items(), key=lambda x: x[1])
            for sid, _ in sorted_by_time[:len(self.sessions) - MAX_SESSIONS]:
                self.sessions.pop(sid, None)
                self.session_times.pop(sid, None)

    def _fallback_reply(self, message: str) -> str:
        message_lower = message.lower()

        if any(kata in message_lower for kata in ["halo", "hai", "hey", "hi", "hii", "helo"]):
            return "Halo! 👋 Ada yang bisa aku bantu pelajari hari ini?"

        if any(kata in message_lower for kata in ["siapa", "nama", "kamu"]):
            return "Aku MetaLearn AI 🤖 — asisten belajarmu yang siap membantu memahami materi pelajaran!"

        if any(kata in message_lower for kata in ["fotosintesis", "fotosintesa"]):
            return (
                "Fotosintesis adalah proses tumbuhan membuat makanan sendiri menggunakan cahaya matahari! ☀️🌱\n\n"
                "Secara sederhana:\n"
                "1. Tumbuhan menyerap air (H₂O) dari akar\n"
                "2. Menyerap karbon dioksida (CO₂) dari udara\n"
                "3. Dengan bantuan cahaya matahari dan klorofil, tumbuhan mengubahnya menjadi glukosa (makanan) dan oksigen\n\n"
                "Reaksi kimianya:\n"
                "6 CO₂ + 6 H₂O → C₆H₁₂O₆ + 6 O₂\n\n"
                "Keren kan? 🌿 Ada yang mau ditanyakan lagi?"
            )

        if any(kata in message_lower for kata in ["matematika", "math", "mtk", "aljabar", "kalkulus", "trigonometri", "rumus"]):
            return (
                "Matematika seru lho! 🎯\n\n"
                "Coba bilang topik spesifik yang mau dipelajari:\n"
                "• Aljabar (persamaan, fungsi)\n"
                "• Geometri (bangun ruang, sudut)\n"
                "• Trigonometri (sin, cos, tan)\n"
                "• Kalkulus (turunan, integral)\n"
                "• Statistika (rata-rata, median, modus)\n\n"
                "Atau kamu punya soal yang mau dibahas bareng? ✨"
            )

        if any(kata in message_lower for kata in ["fisika", "fisik", "hukum", "gerak", "gaya", "energi", "listrik"]):
            return (
                "Fisika itu asyik! ⚡ Mari bahas:\n\n"
                "• Mekanika (gerak, gaya, hukum Newton)\n"
                "• Termodinamika (kalor, suhu)\n"
                "• Listrik & Magnet\n"
                "• Gelombang & Bunyi\n"
                "• Optika (cahaya, lensa)\n\n"
                "Bagian mana yang ingin kamu pelajari? 🚀"
            )

        if any(kata in message_lower for kata in ["biologi", "bio", "sel", "evolusi", "ekosistem", "genetika"]):
            return (
                "Biologi itu seru! 🧬 Yuk bahas:\n\n"
                "• Sel & Jaringan\n"
                "• Genetika (DNA, pewarisan sifat)\n"
                "• Ekosistem & Lingkungan\n"
                "• Evolusi\n"
                "• Sistem tubuh manusia\n\n"
                "Ada topik tertentu yang menarik buatmu? 🔬"
            )

        if any(kata in message_lower for kata in ["kimia", "reaksi", "atom", "molekul", "tabel periodik", "unsur"]):
            return (
                "Kimia itu menarik! 🧪 Ayo pelajari:\n\n"
                "• Struktur atom & tabel periodik\n"
                "• Ikatan kimia\n"
                "• Reaksi kimia & persamaan\n"
                "• Larutan & konsentrasi\n"
                "• Kimia organik\n\n"
                "Ada yang mau ditanyakan? 🔬"
            )

        if any(kata in message_lower for kata in ["bahasa inggris", "english", "grammar", "vocabulary", "tenses"]):
            return (
                "Belajar Bahasa Inggris? 🇬🇧 Yuk!\n\n"
                "Aku bisa bantu:\n"
                "• Grammar & Tenses\n"
                "• Vocabulary & Idioms\n"
                "• Cara bikin kalimat\n"
                "• Reading comprehension\n"
                "• Listening tips\n\n"
                "Mau mulai dari mana? 📚"
            )

        if any(kata in message_lower for kata in ["terima kasih", "thanks", "makasih", "thank"]):
            return "Sama-sama! 😊 Senang bisa membantu. Kalau ada pertanyaan lain, bilang aja ya!"

        if any(kata in message_lower for kata in ["soal", "quiz", "kuis", "latihan", "tryout", "try out", "ujian"]):
            return (
                "Siap latihan soal! 💪\n\n"
                "Katakan topik dan tingkat kesulitannya:\n"
                "• Contoh: \"Soal matematika kelas 10\"\n"
                "• Atau: \"Latihan fisika tentang gerak\"\n\n"
                "Aku akan bantu kamu berlatih! 📝"
            )

        return (
            "Wah, menarik! 🤔\n\n"
            "Aku bisa bantu kamu belajar berbagai mata pelajaran seperti Matematika, Fisika, Kimia, Biologi, "
            "Bahasa Inggris, dan lainnya.\n\n"
            "Coba tanya spesifik tentang topik yang mau kamu pelajari, ya! 📚✨"
        )

    def send_message(self, message: str, session_id: str | None = None) -> dict:
        self._evict_stale_sessions()
        if not session_id:
            session_id = str(uuid.uuid4())

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.session_times[session_id] = time.time()

        history = self.sessions[session_id]
        history.append({"role": "user", "content": message})

        if self.gemini_available:
            prompt = (
                "Kamu adalah MetaLearn AI — asisten pembelajaran adaptif untuk siswa sekolah menengah Indonesia. "
                "Gunakan bahasa Indonesia yang ramah, hangat, dan mudah dipahami oleh remaja. "
                "Kamu membantu siswa memahami materi pelajaran, menjawab pertanyaan, dan memberikan motivasi belajar.\n\n"
                "Panduan:\n"
                "- Jawab dengan jelas dan mendidik, berikan contoh sederhana jika relevan\n"
                "- Jika ditanya di luar materi pelajaran, arahkan kembali ke topik belajar dengan ramah\n"
                "- Jika siswa tampak kesulitan, berikan semangat dan saran langkah selanjutnya\n"
                "- Gunakan emoji sesekali\n"
                "- Jangan berikan jawaban langsung untuk soal ujian — bimbing siswa menemukan jawabannya sendiri\n\n"
            )

            if history:
                prompt += "Riwayat percakapan:\n"
                for msg in history[-10:]:
                    role = "Siswa" if msg["role"] == "user" else "MetaLearn AI"
                    prompt += f"{role}: {msg['content']}\n"
                prompt += "\n"

            prompt += f"Pesan siswa: {message}\n\nMetaLearn AI:"

            try:
                response = self.model.generate_content(prompt)
                answer = response.text if response.text else self._fallback_reply(message)
            except Exception:
                answer = self._fallback_reply(message)
        else:
            answer = self._fallback_reply(message)

        history.append({"role": "assistant", "content": answer})

        return {
            "reply": answer,
            "session_id": session_id,
        }

    def reset_session(self, session_id: str) -> dict:
        if session_id in self.sessions:
            self.sessions.pop(session_id, None)
            self.session_times.pop(session_id, None)
            return {"message": "Percakapan telah direset.", "session_id": session_id}
        return {"message": "Sesi tidak ditemukan.", "session_id": session_id}
