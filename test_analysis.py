import json
from pathlib import Path
from datetime import datetime
from app.services.parser_service import WhatsAppParser
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

from app.services.AnalysisService import AnalysisService


def build_analysis_service():
    return AnalysisService(
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


def test_full_pipeline():

    # -------------------------
    # Load Chat File
    # -------------------------
    content = Path("WhatsApp Chat with QC RizzASs 2024-25.txt").read_text(
        encoding="utf-8"
    )

    parser = WhatsAppParser()
    parsed = parser.parse(content)

    # -------------------------
    # Run Analysis
    # -------------------------
    analysis_service = build_analysis_service()
    result = analysis_service.run(parsed, universe="mcu")

    # -------------------------
    # Basic Assertions
    # -------------------------
    assert "traits" in result
    assert "behavior" in result
    assert "pair_dynamics" in result
    assert "group_health" in result
    assert "risk_analysis" in result
    assert "user_summaries" in result
    assert "explanations" in result

    # -------------------------
    # Save Output to File
    # -------------------------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"analysis_output_{timestamp}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n✅ PIPELINE WORKING")
    print(f"📁 Output saved to: {output_path.resolve()}")


if __name__ == "__main__":
    test_full_pipeline()
