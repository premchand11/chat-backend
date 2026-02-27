import statistics


class GroupHealthEngine:

    def run(self, behavior: dict, pairs: list) -> dict:

        if not behavior:
            return self._empty_result()

        investments = [
            max(0, min(v.get("investment", 0), 1)) for v in behavior.values()
        ]

        dominance = [max(0, min(v.get("dominance", 0), 1)) for v in behavior.values()]

        ghost_scores = [
            max(0, min(v.get("ghost_score", 0), 1)) for v in behavior.values()
        ]

        dry_scores = [
            max(0, min(v.get("dry_text_score", 0), 1)) for v in behavior.values()
        ]

        # ---- Investment Balance ----
        investment_balance = self._balance_score(investments)

        # ---- Dominance Balance ----
        dominance_balance = self._balance_score(dominance)

        # ---- Compatibility ----
        compat_values = [max(0, min(p.get("compatibility", 0), 1)) for p in pairs]

        compat_avg = sum(compat_values) / len(compat_values) if compat_values else 0

        # ---- Ghost Stability ----
        ghost_avg = sum(ghost_scores) / len(ghost_scores) if ghost_scores else 0
        ghost_stability = 1 - ghost_avg

        # ---- Emotional Expressiveness ----
        dry_avg = sum(dry_scores) / len(dry_scores) if dry_scores else 0
        expressiveness = 1 - dry_avg

        # ---- Final Score ----
        health_score = (
            0.25 * investment_balance
            + 0.20 * dominance_balance
            + 0.25 * compat_avg
            + 0.15 * ghost_stability
            + 0.15 * expressiveness
        )

        health_score = max(0, min(health_score, 1))

        return {
            "health_score": round(health_score, 3),
            "investment_balance": round(investment_balance, 3),
            "dominance_balance": round(dominance_balance, 3),
            "compatibility_avg": round(compat_avg, 3),
            "ghost_stability": round(ghost_stability, 3),
            "expressiveness": round(expressiveness, 3),
        }

    def _balance_score(self, values: list) -> float:
        if not values:
            return 0
        if len(values) == 1:
            return 1  # Single user = perfectly balanced

        std = statistics.pstdev(values)
        return 1 - min(std, 1)

    def _empty_result(self):
        return {
            "health_score": 0,
            "investment_balance": 0,
            "dominance_balance": 0,
            "compatibility_avg": 0,
            "ghost_stability": 0,
            "expressiveness": 0,
        }
