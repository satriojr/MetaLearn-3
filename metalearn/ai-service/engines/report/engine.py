import json
from datetime import datetime
from typing import Optional

from engines.gemini import get_gemini_model


class NarrativeReportEngine:
    def __init__(self):
        self.model = get_gemini_model()

    def generate_report(
        self,
        student_name: str,
        mastery_scores: dict,
        gamification: dict,
        recent_activity: list,
        memory: str = "",
    ) -> str:
        prompt = (
            f"Buat laporan perkembangan belajar untuk {student_name} dalam Bahasa Indonesia.\n\n"
            f"Skor penguasaan per topik: {json.dumps(mastery_scores, indent=2)}\n"
            f"Data gamifikasi: {json.dumps(gamification, indent=2)}\n"
            f"Aktivitas terbaru: {json.dumps(recent_activity, indent=2)}\n"
            f"Memori belajar: {memory}\n\n"
            "Buat laporan naratif yang mencakup:\n"
            "1. **Ringkasan Progres** — gambaran umum kemajuan (2-3 kalimat)\n"
            "2. **Area Kekuatan** — topik yang sudah dikuasai dengan baik\n"
            "3. **Area Pengembangan** — topik yang perlu diperbaiki\n"
            "4. **Aktivitas Terkini** — apa yang dikerjakan akhir-akhir ini\n"
            "5. **Rekomendasi** — 3 saran konkret untuk sesi berikutnya\n"
            "6. **Motivasi** — satu kalimat penyemangat\n\n"
            "Gunakan bahasa yang hangat dan mendorong semangat belajar."
        )

        response = self.model.generate_content(prompt)
        return response.text if response.text else "Laporan tidak tersedia."

    def generate_report_html(self, student_name: str, mastery_scores: dict, gamification: dict) -> str:
        report_md = self.generate_report(student_name, mastery_scores, gamification)

        html_prompt = (
            f"Konversi laporan Markdown berikut ke HTML yang bersih dan responsif:\n\n{report_md}\n\n"
            "Gunakan style sederhana dengan warna biru/indigo sebagai aksen. "
            "Output hanya HTML tanpa markdown formatting."
        )

        response = self.model.generate_content(html_prompt)
        return response.text if response.text else "<p>Laporan tidak tersedia.</p>"
