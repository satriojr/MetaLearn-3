"""
Abstract Syntax Tree (AST) Evaluator Engine.

Evaluates student answers by comparing their structural/logical
representation against the expected answer structure.

Supports mathematical expressions, short answers, and code snippets.
This simplified implementation uses a combination of:
1. Token-based structural comparison
2. Normalized semantic equivalence
3. Gemini AI fallback for complex evaluation
"""

import os
import re
import json
from typing import Optional

import google.generativeai as genai


class ASTEvaluator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def evaluate(self, student_answer: str, correct_answer: str, question_text: str) -> dict:
        exact_match = student_answer.strip().lower() == correct_answer.strip().lower()
        if exact_match:
            return {
                "is_correct": True,
                "score": 100,
                "confidence": 1.0,
                "feedback": "Jawaban tepat!",
            }

        normalized_match = self._normalized_compare(student_answer, correct_answer)
        if normalized_match:
            return {
                "is_correct": True,
                "score": 100,
                "confidence": 0.95,
                "feedback": "Jawaban benar secara konseptual!",
            }

        return self._evaluate_with_ai(student_answer, correct_answer, question_text)

    def evaluate_structure(self, answer_structure: dict, expected_structure: dict) -> dict:
        result = self._compare_structures(answer_structure, expected_structure)
        return result

    def _normalized_compare(self, student: str, correct: str) -> bool:
        def normalize(s: str) -> str:
            s = s.lower().strip()
            s = re.sub(r'\s+', ' ', s)
            s = re.sub(r'[^\w\s]', '', s)
            s = re.sub(r'\b(dengan|dan|atau|yang|di|ke|dari)\b', '', s)
            return s.strip()

        return normalize(student) == normalize(correct)

    def _tokenize_structure(self, text: str) -> list:
        tokens = re.findall(r'\b\w+\b|[+\-*/=(){}[\]<>]', text)
        return tokens

    def _structural_similarity(self, tokens1: list, tokens2: list) -> float:
        if not tokens1 or not tokens2:
            return 0.0

        set1, set2 = set(tokens1), set(tokens2)
        intersection = set1 & set2
        union = set1 | set2

        if not union:
            return 0.0

        jaccard = len(intersection) / len(union)
        length_ratio = min(len(tokens1), len(tokens2)) / max(len(tokens1), len(tokens2))

        return (jaccard * 0.6 + length_ratio * 0.4)

    def _compare_structures(self, student: dict, expected: dict) -> dict:
        matched_keys = 0
        total_keys = len(expected)
        mismatches = []

        for key, expected_value in expected.items():
            student_value = student.get(key)
            if student_value == expected_value:
                matched_keys += 1
            elif isinstance(expected_value, dict) and isinstance(student_value, dict):
                sub_result = self._compare_structures(student_value, expected_value)
                if sub_result["is_correct"]:
                    matched_keys += 1
                else:
                    mismatches.append(key)
            else:
                mismatches.append(key)

        if total_keys == 0:
            return {"is_correct": True, "score": 100, "confidence": 1.0, "feedback": "Struktur valid."}

        score = int((matched_keys / total_keys) * 100)
        is_correct = score >= 80

        return {
            "is_correct": is_correct,
            "score": score,
            "confidence": score / 100,
            "feedback": f"Struktur jawaban {'benar' if is_correct else 'kurang tepat'}. "
                        f"{matched_keys}/{total_keys} komponen sesuai."
                        + (f" Periksa: {', '.join(mismatches)}" if mismatches else ""),
        }

    def _evaluate_with_ai(self, student_answer: str, correct_answer: str, question_text: str) -> dict:
        prompt = (
            f"Evaluasi jawaban siswa berikut secara konseptual:\n\n"
            f"Soal: {question_text}\n"
            f"Jawaban benar: {correct_answer}\n"
            f"Jawaban siswa: {student_answer}\n\n"
            "Apakah jawaban siswa benar secara konseptual (meski tidak persis sama)?\n"
            "Respond in JSON format:\n"
            '{"is_correct": true/false, "score": 0-100, "confidence": 0.0-1.0, '
            '"feedback": "penjelasan dalam Bahasa Indonesia", '
            '"concept_match": "seberapa dekat konsepnya, deskriptif"}'
        )

        try:
            response = self.model.generate_content(prompt)
            text = response.text if response.text else "{}"
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except (json.JSONDecodeError, Exception):
            return {
                "is_correct": False,
                "score": 0,
                "confidence": 0.0,
                "feedback": "Gagal mengevaluasi jawaban.",
            }
