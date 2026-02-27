class UserSummaryEngine:

    def run(self, behavior: dict, pairs: list, traits: dict) -> dict:

        if not behavior:
            return {}

        summaries = {}

        # ---- Rankings ----
        dominance_sorted = sorted(
            behavior.items(),
            key=lambda x: x[1].get("dominance", 0),
            reverse=True,
        )

        investment_sorted = sorted(
            behavior.items(),
            key=lambda x: x[1].get("investment", 0),
            reverse=True,
        )

        influence_scores = {
            name: self._clamp(
                (data.get("dominance", 0) + data.get("investment", 0)) / 2
            )
            for name, data in behavior.items()
        }

        influence_sorted = sorted(
            influence_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        dominance_rank = {name: i + 1 for i, (name, _) in enumerate(dominance_sorted)}
        investment_rank = {name: i + 1 for i, (name, _) in enumerate(investment_sorted)}
        influence_rank = {name: i + 1 for i, (name, _) in enumerate(influence_sorted)}

        for name in behavior.keys():

            user_pairs = [
                p for p in pairs if name in (p.get("user_a"), p.get("user_b"))
            ]

            strongest_partner = None
            most_imbalanced_data = None

            if user_pairs:

                strongest = max(
                    user_pairs,
                    key=lambda x: x.get("compatibility", 0),
                )

                strongest_partner = (
                    strongest["user_b"]
                    if strongest["user_a"] == name
                    else strongest["user_a"]
                )

                sorted_by_diff = sorted(
                    user_pairs,
                    key=lambda x: x.get("investment_diff", 0),
                    reverse=True,
                )

                significant = [
                    p for p in sorted_by_diff if p.get("investment_diff", 0) > 0.2
                ]

                most_imbalanced = significant[0] if significant else sorted_by_diff[0]

                partner = (
                    most_imbalanced["user_b"]
                    if most_imbalanced["user_a"] == name
                    else most_imbalanced["user_a"]
                )

                user_inv = behavior.get(name, {}).get("investment", 0)
                partner_inv = behavior.get(partner, {}).get("investment", 0)

                if user_inv > partner_inv:
                    imbalance_direction = "You invest more"
                elif user_inv < partner_inv:
                    imbalance_direction = "They invest more"
                else:
                    imbalance_direction = "Balanced effort"

                most_imbalanced_data = {
                    "partner": partner,
                    "investment_diff": round(
                        most_imbalanced.get("investment_diff", 0),
                        3,
                    ),
                    "direction": imbalance_direction,
                }

            risk_flag = self._risk_flag(name, behavior)
            role = self._role_label(name, behavior, traits)

            summaries[name] = {
                "dominance_rank": dominance_rank.get(name),
                "investment_rank": investment_rank.get(name),
                "influence_rank": influence_rank.get(name),
                "influence_score": round(influence_scores.get(name, 0), 3),
                "strongest_bond": strongest_partner,
                "most_imbalanced_bond": most_imbalanced_data,
                "role": role,
                "risk_flag": risk_flag,
            }

        return summaries

    # -------------------------
    # Risk Flags
    # -------------------------

    def _risk_flag(self, name: str, behavior: dict) -> str:

        b = behavior.get(name, {})

        if b.get("ghost_score", 0) > 0.8:
            return "High Ghost Risk"

        if b.get("dominance", 0) > 0.85:
            return "High Control Influence"

        if b.get("dry_text_score", 0) > 0.85:
            return "Emotionally Reserved"

        if b.get("investment", 1) < 0.2:
            return "Low Emotional Investment"

        return "Stable Presence"

    # -------------------------
    # Role Labels
    # -------------------------

    def _role_label(self, name: str, behavior: dict, traits: dict) -> str:

        b = behavior.get(name, {})
        t = traits.get(name, {})

        if b.get("dominance", 0) > 0.85:
            return "Alpha Leader"

        if b.get("dominance", 0) > 0.7 and b.get("investment", 0) > 0.5:
            return "Strategic Driver"

        if b.get("investment", 0) > 0.6 and t.get("warmth", 0) > 0.7:
            return "Emotional Anchor"

        if t.get("stability", 0) > 0.8:
            return "Stability Pillar"

        if b.get("ghost_score", 0) > 0.8:
            return "Unpredictable Presence"

        if b.get("dry_text_score", 0) > 0.85:
            return "Silent Analyzer"

        if t.get("mystery", 0) > 0.8:
            return "Enigmatic Member"

        return "Active Contributor"

    def _clamp(self, value: float) -> float:
        return max(0.0, min(value, 1.0))


# class UserSummaryEngine:

#     def compute(self, behavior: dict, pairs: list, traits: dict) -> dict:

#         summaries = {}

#         # ---- Rankings ----
#         dominance_sorted = sorted(
#             behavior.items(), key=lambda x: x[1]["dominance"], reverse=True
#         )

#         investment_sorted = sorted(
#             behavior.items(), key=lambda x: x[1]["investment"], reverse=True
#         )

#         # 🔥 Influence = (dominance + investment) / 2
#         influence_scores = {
#             name: (data["dominance"] + data["investment"]) / 2
#             for name, data in behavior.items()
#         }

#         influence_sorted = sorted(
#             influence_scores.items(), key=lambda x: x[1], reverse=True
#         )

#         dominance_rank = {name: i + 1 for i, (name, _) in enumerate(dominance_sorted)}
#         investment_rank = {name: i + 1 for i, (name, _) in enumerate(investment_sorted)}
#         influence_rank = {name: i + 1 for i, (name, _) in enumerate(influence_sorted)}

#         # ---- Per User Summary ----
#         for name in behavior.keys():

#             user_pairs = [p for p in pairs if name in p["pair"]]

#             # ---- Strongest Bond ----
#             strongest = max(user_pairs, key=lambda x: x["compatibility"])

#             strongest_partner = (
#                 strongest["pair"][0]
#                 if strongest["pair"][1] == name
#                 else strongest["pair"][1]
#             )

#             # ---- Most Imbalanced Bond (Directional Logic) ----
#             sorted_by_diff = sorted(
#                 user_pairs, key=lambda x: x["investment_diff"], reverse=True
#             )

#             significant = [p for p in sorted_by_diff if p["investment_diff"] > 0.2]

#             if significant:
#                 most_imbalanced = significant[0]
#             else:
#                 most_imbalanced = sorted_by_diff[0]

#             partner = (
#                 most_imbalanced["pair"][0]
#                 if most_imbalanced["pair"][1] == name
#                 else most_imbalanced["pair"][1]
#             )

#             user_investment = behavior[name]["investment"]
#             partner_investment = behavior[partner]["investment"]

#             if user_investment > partner_investment:
#                 imbalance_direction = "You invest more"
#             elif user_investment < partner_investment:
#                 imbalance_direction = "They invest more"
#             else:
#                 imbalance_direction = "Balanced effort"

#             # ---- Risk Flag ----
#             risk_flag = self._risk_flag(name, behavior, traits)

#             # ---- Role Label ----
#             role = self._role_label(name, behavior, traits)

#             summaries[name] = {
#                 "dominance_rank": dominance_rank[name],
#                 "investment_rank": investment_rank[name],
#                 "influence_rank": influence_rank[name],
#                 "influence_score": round(influence_scores[name], 3),
#                 "strongest_bond": strongest_partner,
#                 "most_imbalanced_bond": {
#                     "partner": partner,
#                     "investment_diff": round(most_imbalanced["investment_diff"], 3),
#                     "direction": imbalance_direction,
#                 },
#                 "role": role,
#                 "risk_flag": risk_flag,
#             }

#         return summaries

#     # -------------------------
#     # Risk Flags
#     # -------------------------

#     def _risk_flag(self, name: str, behavior: dict, traits: dict) -> str:

#         b = behavior[name]

#         if b["ghost_score"] > 0.8:
#             return "High Ghost Risk"

#         if b["dominance"] > 0.85:
#             return "High Control Influence"

#         if b["dry_text_score"] > 0.85:
#             return "Emotionally Reserved"

#         if b["investment"] < 0.2:
#             return "Low Emotional Investment"

#         return "Stable Presence"

#     # -------------------------
#     # Role Labels
#     # -------------------------

#     def _role_label(self, name: str, behavior: dict, traits: dict) -> str:

#         b = behavior[name]
#         t = traits[name]

#         if b["dominance"] > 0.85:
#             return "Alpha Leader"

#         if b["dominance"] > 0.7 and b["investment"] > 0.5:
#             return "Strategic Driver"

#         if b["investment"] > 0.6 and t["warmth"] > 0.7:
#             return "Emotional Anchor"

#         if t["stability"] > 0.8:
#             return "Stability Pillar"

#         if b["ghost_score"] > 0.8:
#             return "Unpredictable Presence"

#         if b["dry_text_score"] > 0.85:
#             return "Silent Analyzer"

#         if t["mystery"] > 0.8:
#             return "Enigmatic Member"

#         return "Active Contributor"
