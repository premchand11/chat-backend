# app/services/analysis_service.py


class AnalysisService:

    def __init__(
        self,
        metrics_engine,
        trait_engine,
        universe_engine,
        behavior_engine,
        engagement_engine,
        linguistic_engine,
        trend_engine,
        pair_engine,
        character_engine,
        explanation_engine,
        group_health_engine,
        risk_engine,
        user_summary_engine,
    ):
        self.metrics_engine = metrics_engine
        self.trait_engine = trait_engine
        self.universe_engine = universe_engine
        self.behavior_engine = behavior_engine
        self.engagement_engine = engagement_engine
        self.linguistic_engine = linguistic_engine
        self.trend_engine = trend_engine
        self.pair_engine = pair_engine
        self.character_engine = character_engine
        self.explanation_engine = explanation_engine
        self.group_health_engine = group_health_engine
        self.risk_engine = risk_engine
        self.user_summary_engine = user_summary_engine

    def run(self, parsed_data: dict, universe: str = "mcu") -> dict:

        metrics = self.metrics_engine.run(parsed_data)
        base_traits = self.trait_engine.run(metrics)

        adjusted_traits = self.universe_engine.run(
            base_traits,
            universe=universe,
        )

        behavior = self.behavior_engine.run(metrics, adjusted_traits)
        engagement = self.engagement_engine.run(parsed_data)

        pairs = self.pair_engine.run(adjusted_traits, behavior)
        linguistics = self.linguistic_engine.run(parsed_data)
        trends = self.trend_engine.run(parsed_data)

        character_matches = self.character_engine.run(adjusted_traits)

        group_health = self.group_health_engine.run(behavior, pairs)

        risk_analysis = self.risk_engine.run(
            behavior,
            pairs,
            adjusted_traits,
        )

        user_summaries = self.user_summary_engine.run(
            behavior,
            pairs,
            adjusted_traits,
        )

        explanations = {
            name: self.explanation_engine.run(
                name=name,
                traits=adjusted_traits.get(name, {}),
                character=match.get("character"),
                confidence=match.get("confidence", 0),
            )
            for name, match in character_matches.items()
        }

        return {
            "meta": {
                "universe": universe,
                "participants": parsed_data.get("participants", []),
            },
            "chat_metrics": metrics.get("chat_metrics", {}),
            "traits": adjusted_traits,
            "behavior": behavior,
            "engagement": engagement,
            "pair_dynamics": pairs,
            "group_health": group_health,
            "risk_analysis": risk_analysis,
            "trends": trends,
            "linguistics": linguistics,
            "character_matches": character_matches,
            "user_summaries": user_summaries,
            "explanations": explanations,
        }
