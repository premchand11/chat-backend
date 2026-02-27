from fastapi import APIRouter, UploadFile, File, Query, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.chat_analysis import ChatAnalysis

from app.services.parser_service import WhatsAppParser
from app.services.AnalysisService import AnalysisService
from app.services.ai_service import AIService

from app.engines.metrics_engine import MetricsEngine
from app.engines.trait_engine import TraitEngine
from app.engines.universe_engine import UniverseEngine
from app.engines.behavior_engine import BehaviorEngine
from app.engines.engagement_engine import EngagementEngine
from app.engines.linguistic_engine import LinguisticEngine
from app.engines.trend_engine import TrendEngine
from app.engines.pair_engine import PairDynamicsEngine
from app.engines.character_engine import CharacterEngine
from app.engines.explanation_engine import ExplanationEngine
from app.engines.group_health_engine import GroupHealthEngine
from app.engines.risk_engine import RiskEngine
from app.engines.user_summary_engine import UserSummaryEngine

from app.services.ai_payload_builder import (
    build_user_payload_from_analysis,
    build_group_payload_from_analysis,
)

from app.services.analysis_orchestrator import run_full_analysis

router = APIRouter(prefix="/analysis", tags=["analysis"])


# ---- Instantiate Core Services Once ----
parser = WhatsAppParser()

analysis_service = AnalysisService(
    metrics_engine=MetricsEngine(),
    trait_engine=TraitEngine(),
    universe_engine=UniverseEngine(),
    behavior_engine=BehaviorEngine(),
    engagement_engine=EngagementEngine(),
    linguistic_engine=LinguisticEngine(),
    trend_engine=TrendEngine(),
    pair_engine=PairDynamicsEngine(),
    character_engine=CharacterEngine(),
    explanation_engine=ExplanationEngine(),
    group_health_engine=GroupHealthEngine(),
    risk_engine=RiskEngine(),
    user_summary_engine=UserSummaryEngine(),
)

ai_service = AIService(api_key=settings.GROQ_API_KEY)  # Use config internally


# ---- Safe AI Wrapper ----
async def generate_ai_layer_safe(analysis: dict):

    try:
        user_payload = build_user_payload_from_analysis(analysis)
        group_payload = build_group_payload_from_analysis(analysis)

        ai_users = await ai_service.generate_user_summaries(user_payload)
        ai_group = await ai_service.generate_group_summary(group_payload)

        return {
            "status": "complete",
            "group_summary": ai_group,
            "users": ai_users,
        }

    except Exception:
        return {
            "status": "failed",
            "group_summary": None,
            "users": {},
        }


# ---- Main Endpoint ----
@router.post("/upload")
async def analyze_chat(
    file: UploadFile = File(...),
    universe: str = Query("mcu"),
    db: Session = Depends(get_db),
):

    content = (await file.read()).decode("utf-8")
    parsed = parser.parse(content)

    analysis = await run_full_analysis(
        parsed_data=parsed,
        universe=universe,
        analysis_service=analysis_service,
        ai_service=ai_service,
    )

    # Save to DB
    record = ChatAnalysis(
        universe=universe,
        participants_count=len(parsed.get("participants", [])),
        analysis=analysis,
    )

    db.add(record)
    db.commit()

    return analysis
