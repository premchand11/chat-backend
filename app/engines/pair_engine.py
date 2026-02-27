from itertools import combinations


class PairDynamicsEngine:

    REQUIRED_TRAITS = ["warmth", "stability", "intensity", "mystery", "control"]

    def run(self, traits: dict, behavior: dict) -> list:

        if not traits:
            return []

        results = []

        for (name1, traits1), (name2, traits2) in combinations(traits.items(), 2):

            t1 = self._safe_traits(traits1)
            t2 = self._safe_traits(traits2)

            compatibility = self._compatibility_score(t1, t2)
            dynamic_type = self._dynamic_type(t1, t2)

            inv1 = behavior.get(name1, {}).get("investment", 0)
            inv2 = behavior.get(name2, {}).get("investment", 0)

            investment_diff = abs(inv1 - inv2)

            if investment_diff > 0.30:
                imbalance_type = "One-Sided Dynamic"
            elif investment_diff > 0.15:
                imbalance_type = "Uneven Effort"
            else:
                imbalance_type = "Mutual Investment"

            results.append(
                {
                    "user_a": name1,
                    "user_b": name2,
                    "compatibility": round(compatibility, 3),
                    "dynamic": dynamic_type,
                    "investment_diff": round(investment_diff, 3),
                    "investment_dynamic": imbalance_type,
                }
            )

        results.sort(key=lambda x: x["compatibility"], reverse=True)

        return results

    def _safe_traits(self, traits: dict) -> dict:
        return {t: max(0, min(traits.get(t, 0), 1)) for t in self.REQUIRED_TRAITS}

    def _compatibility_score(self, t1: dict, t2: dict) -> float:

        warmth_score = 1 - abs(t1["warmth"] - t2["warmth"])
        stability_score = 1 - abs(t1["stability"] - t2["stability"])
        intensity_balance = 1 - abs(t1["intensity"] - t2["intensity"])
        mystery_balance = 1 - abs(t1["mystery"] - t2["mystery"])

        control_clash = t1["control"] * t2["control"]

        score = (
            0.30 * warmth_score
            + 0.25 * stability_score
            + 0.20 * intensity_balance
            + 0.15 * mystery_balance
            - 0.10 * control_clash
        )

        return max(0, min(score, 1))

    def _dynamic_type(self, t1: dict, t2: dict) -> str:

        if t1["control"] > 0.7 and t2["control"] > 0.7:
            return "Power Struggle"

        if t1["intensity"] > 0.7 and t2["intensity"] > 0.7:
            return "Explosive Energy"

        if t1["warmth"] > 0.7 and t2["warmth"] > 0.7:
            return "Emotional Sync"

        if t1["stability"] > 0.7 and t2["stability"] > 0.7:
            return "Calm Anchors"

        if abs(t1["intensity"] - t2["intensity"]) > 0.5:
            return "Opposites Attract"

        return "Balanced Dynamic"


# from itertools import combinations


# class PairDynamicsEngine:

#     def compute(self, traits: dict, behavior: dict) -> list:

#         results = []

#         for (name1, traits1), (name2, traits2) in combinations(traits.items(), 2):

#             compatibility = self._compatibility_score(traits1, traits2)
#             dynamic_type = self._dynamic_type(traits1, traits2)

#             # 🔥 Investment imbalance
#             investment_diff = abs(
#                 behavior[name1]["investment"] - behavior[name2]["investment"]
#             )

#             if investment_diff > 0.30:
#                 imbalance_type = "One-Sided Dynamic"
#             elif investment_diff > 0.15:
#                 imbalance_type = "Uneven Effort"
#             else:
#                 imbalance_type = "Mutual Investment"

#             results.append(
#                 {
#                     "pair": (name1, name2),
#                     "compatibility": round(compatibility, 3),
#                     "dynamic": dynamic_type,
#                     "investment_diff": round(investment_diff, 3),
#                     "investment_dynamic": imbalance_type,
#                 }
#             )

#         # Sort by compatibility descending
#         results.sort(key=lambda x: x["compatibility"], reverse=True)

#         return results

#     def _compatibility_score(self, t1: dict, t2: dict) -> float:

#         warmth_score = 1 - abs(t1["warmth"] - t2["warmth"])
#         stability_score = 1 - abs(t1["stability"] - t2["stability"])
#         intensity_balance = 1 - abs(t1["intensity"] - t2["intensity"])
#         mystery_balance = 1 - abs(t1["mystery"] - t2["mystery"])

#         control_clash = t1["control"] * t2["control"]

#         score = (
#             0.30 * warmth_score
#             + 0.25 * stability_score
#             + 0.20 * intensity_balance
#             + 0.15 * mystery_balance
#             - 0.10 * control_clash
#         )

#         return max(0, min(score, 1))

#     def _dynamic_type(self, t1: dict, t2: dict) -> str:

#         if t1["control"] > 0.7 and t2["control"] > 0.7:
#             return "Power Struggle"

#         if t1["intensity"] > 0.7 and t2["intensity"] > 0.7:
#             return "Explosive Energy"

#         if t1["warmth"] > 0.7 and t2["warmth"] > 0.7:
#             return "Emotional Sync"

#         if t1["stability"] > 0.7 and t2["stability"] > 0.7:
#             return "Calm Anchors"

#         if abs(t1["intensity"] - t2["intensity"]) > 0.5:
#             return "Opposites Attract"

#         return "Balanced Dynamic"
