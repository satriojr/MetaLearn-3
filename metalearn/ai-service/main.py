from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from engines.nlp.engine import GeminiNLPEngine
from engines.pathway.engine import AdaptivePathwayEngine
from engines.bkt.engine import BKTEngine
from engines.ast_evaluator.engine import ASTEvaluator
from engines.report.engine import NarrativeReportEngine

app = FastAPI(title="MetaLearn AI Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp_engine = GeminiNLPEngine()
pathway_engine = AdaptivePathwayEngine()
bkt_engine = BKTEngine()
ast_evaluator = ASTEvaluator()
report_engine = NarrativeReportEngine()


# --- Schemas ---

class AskRequest(BaseModel):
    question: str
    mission_context: Optional[str] = None
    memory: Optional[str] = None


class PathwayRequest(BaseModel):
    interests: list[str]
    learning_style: str
    mastery_scores: Optional[dict] = None
    completed_missions: Optional[list] = None


class BKTEvaluateRequest(BaseModel):
    prior_mastery: float = 0.2
    is_correct: bool
    correct_count: Optional[int] = None
    total_count: Optional[int] = None


class ASTEvaluateRequest(BaseModel):
    student_answer: str
    correct_answer: str
    question_text: str


class ReportRequest(BaseModel):
    student_name: str
    mastery_scores: dict
    gamification: dict
    recent_activity: Optional[list] = None
    memory: Optional[str] = None


class SessionSummaryRequest(BaseModel):
    session_data: dict
    memory: Optional[str] = None


class GenerateQuestionsRequest(BaseModel):
    topic: str
    difficulty: str = "intermediate"
    count: int = 5


class RemedialRequest(BaseModel):
    weak_topics: list[str]
    learning_style: str


# --- Routes ---

@app.get("/health")
async def health():
    return {"status": "ok", "service": "metalearn-ai"}


@app.post("/nlp/ask")
async def ask(req: AskRequest):
    try:
        context = {}
        if req.mission_context:
            context["mission_context"] = req.mission_context
        if req.memory:
            context["memory"] = req.memory
        answer = nlp_engine.ask(req.question, context)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/nlp/summary")
async def summary(req: SessionSummaryRequest):
    try:
        summary_text = nlp_engine.generate_summary(req.session_data, req.memory or "")
        return {"summary": summary_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/nlp/generate-questions")
async def generate_questions(req: GenerateQuestionsRequest):
    try:
        questions = nlp_engine.generate_questions(req.topic, req.difficulty, req.count)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pathway/generate")
async def generate_pathway(req: PathwayRequest):
    try:
        result = pathway_engine.generate_pathway(
            interests=req.interests,
            learning_style=req.learning_style,
            mastery_scores=req.mastery_scores,
            completed_missions=req.completed_missions,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pathway/remedial")
async def remedial(req: RemedialRequest):
    try:
        result = pathway_engine.generate_remedial_mission(
            weak_topics=req.weak_topics,
            learning_style=req.learning_style,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/bkt/evaluate")
async def bkt_evaluate(req: BKTEvaluateRequest):
    try:
        if req.correct_count is not None and req.total_count is not None:
            mastery = bkt_engine.estimate_mastery(req.correct_count, req.total_count)
        else:
            mastery = bkt_engine.update_mastery(req.prior_mastery, req.is_correct)

        return {
            "mastery": round(mastery, 4),
            "should_remediate": bkt_engine.should_remediate(mastery),
            "recommended_difficulty": bkt_engine.get_difficulty_adjustment(mastery),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ast/evaluate")
async def ast_evaluate(req: ASTEvaluateRequest):
    try:
        result = ast_evaluator.evaluate(req.student_answer, req.correct_answer, req.question_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/report/generate")
async def generate_report(req: ReportRequest):
    try:
        report = report_engine.generate_report(
            student_name=req.student_name,
            mastery_scores=req.mastery_scores,
            gamification=req.gamification,
            recent_activity=req.recent_activity or [],
            memory=req.memory or "",
        )
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
