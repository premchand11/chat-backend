from typing import Dict


# -----------------------------------------------------
# 🎭 USER PAYLOAD BUILDER
# -----------------------------------------------------


def build_user_payload_from_analysis(analysis: dict) -> Dict:

    traits = analysis.get("traits", {})
    behavior = analysis.get("behavior", {})
    user_summaries = analysis.get("user_summaries", {})
    character_matches = analysis.get("character_matches", {})

    payload = {}

    for name in user_summaries.keys():

        t = traits.get(name, {})
        b = behavior.get(name, {})
        s = user_summaries.get(name, {})
        c = character_matches.get(name, {})

        payload[name] = {
            "name": name,
            "character": c.get("character", "Unknown"),
            "role": s.get("role", "Active Member"),
            "risk_flag": s.get("risk_flag", "Stable Presence"),
            "strongest_bond": s.get("strongest_bond", "Unknown"),
            "traits": _semantic_traits(t),
            "behavior": _semantic_behavior(b),
            "influence_rank": s.get("influence_rank", 999),
        }

    return payload


# -----------------------------------------------------
# 👥 GROUP PAYLOAD BUILDER
# -----------------------------------------------------


def build_group_payload_from_analysis(analysis: dict) -> Dict:

    group_health = analysis.get("group_health", {})
    risk_analysis = analysis.get("risk_analysis", {})
    user_summaries = analysis.get("user_summaries", {})
    trends = analysis.get("trends", {})

    # ---- Top Influencer ----
    if user_summaries:
        top_user = min(
            user_summaries.items(),
            key=lambda x: x[1].get("influence_rank", 999),
        )[0]
    else:
        top_user = "Unknown"

    # ---- Ghost Prone ----
    most_ghost = risk_analysis.get("most_ghost_prone_member", {})
    ghost_name = most_ghost.get("name", "Unknown")

    # ---- Semantic Labels ----
    health_score = group_health.get("health_score", 0)
    night_ratio = trends.get("night_activity_ratio", 0)

    return {
        "top_influencer": top_user,
        "most_ghost_prone": ghost_name,
        "group_energy": _semantic_group_energy(health_score),
        "group_stability": _semantic_night_activity(night_ratio),
    }


# -----------------------------------------------------
# 🔥 Semantic Converters (CRITICAL FOR DRAMATIC AI)
# -----------------------------------------------------


def _semantic_traits(t: dict) -> dict:

    return {
        "intensity": _level_label(t.get("intensity", 0)),
        "warmth": _level_label(t.get("warmth", 0)),
        "control": _level_label(t.get("control", 0)),
        "stability": _level_label(t.get("stability", 0)),
        "mystery": _level_label(t.get("mystery", 0)),
    }


def _semantic_behavior(b: dict) -> dict:

    return {
        "investment": _level_label(b.get("investment", 0)),
        "dominance": _level_label(b.get("dominance", 0)),
        "ghost_score": _reverse_level_label(b.get("ghost_score", 0)),
        "dry_text_score": _reverse_level_label(b.get("dry_text_score", 0)),
    }


def _semantic_group_energy(score: float) -> str:

    if score > 0.75:
        return "remarkably balanced and synchronized"
    if score > 0.5:
        return "energetic but occasionally chaotic"
    if score > 0.3:
        return "unstable and unpredictable"
    return "volatile and fragile"


def _semantic_night_activity(ratio: float) -> str:

    if ratio > 0.6:
        return "thrives deep into the night"
    if ratio > 0.3:
        return "occasionally awakens after dark"
    return "mostly active in daylight hours"


# -----------------------------------------------------
# 📊 Value → Level Mapping
# -----------------------------------------------------


def _level_label(value: float) -> str:

    if value >= 0.8:
        return "very strong"
    if value >= 0.6:
        return "strong"
    if value >= 0.4:
        return "moderate"
    if value >= 0.2:
        return "subtle"
    return "very subtle"


def _reverse_level_label(value: float) -> str:
    """
    For ghost/dry where high value is negative.
    We invert meaning for narrative clarity.
    """

    if value >= 0.8:
        return "frequent"
    if value >= 0.6:
        return "noticeable"
    if value >= 0.4:
        return "occasional"
    if value >= 0.2:
        return "rare"
    return "almost nonexistent"
