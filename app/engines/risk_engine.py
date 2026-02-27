class RiskEngine:

    def run(self, behavior: dict, pairs: list, traits: dict) -> dict:

        if not behavior:
            return self._empty_result()

        # ---- Most One-Sided Pair ----
        most_one_sided = (
            max(pairs, key=lambda x: x.get("investment_diff", 0)) if pairs else None
        )

        # ---- Biggest Power Clash ----
        biggest_power_clash = None
        highest_control_product = -1

        for pair in pairs:
            user_a = pair.get("user_a")
            user_b = pair.get("user_b")

            control_a = self._safe_trait(traits, user_a, "control")
            control_b = self._safe_trait(traits, user_b, "control")

            product = control_a * control_b

            if product > highest_control_product:
                highest_control_product = product
                biggest_power_clash = pair

        # ---- Behavior Extremes ----
        most_ghost = max(
            behavior.items(),
            key=lambda x: x[1].get("ghost_score", 0),
        )

        lowest_investment = min(
            behavior.items(),
            key=lambda x: x[1].get("investment", 0),
        )

        highest_dominance = max(
            behavior.items(),
            key=lambda x: x[1].get("dominance", 0),
        )

        most_dry = max(
            behavior.items(),
            key=lambda x: x[1].get("dry_text_score", 0),
        )

        return {
            "most_one_sided_pair": most_one_sided,
            "biggest_power_clash": biggest_power_clash,
            "most_ghost_prone_member": {
                "name": most_ghost[0],
                "ghost_score": round(
                    max(0, min(most_ghost[1].get("ghost_score", 0), 1)), 3
                ),
            },
            "lowest_investment_member": {
                "name": lowest_investment[0],
                "investment": round(
                    max(0, min(lowest_investment[1].get("investment", 0), 1)), 3
                ),
            },
            "highest_dominance_member": {
                "name": highest_dominance[0],
                "dominance": round(
                    max(0, min(highest_dominance[1].get("dominance", 0), 1)), 3
                ),
            },
            "most_dry_member": {
                "name": most_dry[0],
                "dry_text_score": round(
                    max(0, min(most_dry[1].get("dry_text_score", 0), 1)), 3
                ),
            },
        }

    def _safe_trait(self, traits: dict, name: str, key: str) -> float:
        return max(0, min(traits.get(name, {}).get(key, 0), 1))

    def _empty_result(self):
        return {
            "most_one_sided_pair": None,
            "biggest_power_clash": None,
            "most_ghost_prone_member": None,
            "lowest_investment_member": None,
            "highest_dominance_member": None,
            "most_dry_member": None,
        }


# class RiskEngine:

#     def compute(self, behavior: dict, pairs: list, traits: dict) -> dict:

#         # ---- Most One-Sided Pair ----
#         most_one_sided = max(pairs, key=lambda x: x["investment_diff"])

#         # ---- Biggest Power Clash ----
#         biggest_power_clash = max(
#             pairs,
#             key=lambda x: (
#                 traits[x["pair"][0]]["control"] * traits[x["pair"][1]]["control"]
#             ),
#         )

#         # ---- Most Ghost-Prone Member ----
#         most_ghost = max(behavior.items(), key=lambda x: x[1]["ghost_score"])

#         # ---- Lowest Investment Member ----
#         lowest_investment = min(behavior.items(), key=lambda x: x[1]["investment"])

#         # ---- Highest Dominance Member ----
#         highest_dominance = max(behavior.items(), key=lambda x: x[1]["dominance"])

#         # ---- Most Emotionally Reserved (Highest Dry Score) ----
#         most_dry = max(behavior.items(), key=lambda x: x[1]["dry_text_score"])

#         return {
#             "most_one_sided_pair": most_one_sided,
#             "biggest_power_clash": biggest_power_clash,
#             "most_ghost_prone_member": {
#                 "name": most_ghost[0],
#                 "ghost_score": most_ghost[1]["ghost_score"],
#             },
#             "lowest_investment_member": {
#                 "name": lowest_investment[0],
#                 "investment": lowest_investment[1]["investment"],
#             },
#             "highest_dominance_member": {
#                 "name": highest_dominance[0],
#                 "dominance": highest_dominance[1]["dominance"],
#             },
#             "most_dry_member": {
#                 "name": most_dry[0],
#                 "dry_text_score": most_dry[1]["dry_text_score"],
#             },
#         }
