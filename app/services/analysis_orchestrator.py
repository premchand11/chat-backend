import traceback
from app.services.ai_payload_builder import (
    build_user_payload_from_analysis,
    build_group_payload_from_analysis,
)


async def run_full_analysis(
    parsed_data: dict,
    universe: str,
    analysis_service,
    ai_service,
) -> dict:

    # -------------------------
    # 1️⃣ Deterministic Layer
    # -------------------------
    analysis = analysis_service.run(parsed_data, universe)

    # -------------------------
    # 2️⃣ AI Layer (Safe)
    # -------------------------
    try:
        user_payload = build_user_payload_from_analysis(analysis)
        group_payload = build_group_payload_from_analysis(analysis)

        ai_user_summaries = await ai_service.generate_user_summaries(user_payload)
        ai_group_summary = await ai_service.generate_group_summary(group_payload)

        analysis["ai_insights"] = {
            "status": "complete",
            "group_summary": ai_group_summary,
            "users": ai_user_summaries,
        }
        print("USER PAYLOAD SAMPLE:", list(user_payload.values())[0])

    except Exception as e:
        print("AI LAYER ERROR:", str(e))
        traceback.print_exc()

        analysis["ai_insights"] = {
            "status": "failed",
            "group_summary": None,
            "users": {},
        }

    return analysis
