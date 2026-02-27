# class CharacterEngine:

# MCU_MATRIX = {
#     # 🔥 Dominant + Strategic + Assertive
#     "Iron Man": {
#         "intensity": 0.45,
#         "control": 0.40,
#         "warmth": 0.05,
#         "stability": 0.05,
#         "mystery": 0.05,
#     },
#     # 🛡 Balanced Leader
#     "Captain America": {
#         "warmth": 0.40,
#         "stability": 0.35,
#         "control": 0.15,
#         "intensity": 0.05,
#         "mystery": 0.05,
#     },
#     # 🌀 Strategic + Manipulative
#     "Loki": {
#         "mystery": 0.50,
#         "control": 0.30,
#         "intensity": 0.15,
#         "warmth": 0.025,
#         "stability": 0.025,
#     },
#     # ⚡ Energetic + Loud
#     "Thor": {
#         "intensity": 0.55,
#         "warmth": 0.25,
#         "control": 0.10,
#         "stability": 0.05,
#         "mystery": 0.05,
#     },
#     # 🔮 Calculated + Calm Strategist
#     "Doctor Strange": {
#         "control": 0.45,
#         "mystery": 0.35,
#         "stability": 0.15,
#         "intensity": 0.025,
#         "warmth": 0.025,
#     },
#     # 🕷 Friendly + Playful
#     "Spider-Man": {
#         "warmth": 0.45,
#         "intensity": 0.30,
#         "stability": 0.10,
#         "control": 0.075,
#         "mystery": 0.075,
#     },
#     # 💥 Pure Intensity + Chaos
#     "Hulk": {
#         "intensity": 0.65,
#         "control": 0.05,
#         "warmth": 0.05,
#         "stability": 0.10,
#         "mystery": 0.15,
#     },
#     # 🕶 Silent + Tactical
#     "Black Widow": {
#         "mystery": 0.45,
#         "stability": 0.35,
#         "control": 0.10,
#         "intensity": 0.05,
#         "warmth": 0.05,
#     },
#     # 🧠 Stable + Analytical
#     "Vision": {
#         "stability": 0.55,
#         "warmth": 0.20,
#         "control": 0.10,
#         "intensity": 0.075,
#         "mystery": 0.075,
#     },
#     # 🛰 Master Planner
#     "Nick Fury": {
#         "control": 0.55,
#         "mystery": 0.30,
#         "stability": 0.10,
#         "intensity": 0.025,
#         "warmth": 0.025,
#     },
#     # 🌪 Emotionally Intense + Unpredictable
#     "Scarlet Witch": {
#         "intensity": 0.40,
#         "mystery": 0.35,
#         "warmth": 0.10,
#         "control": 0.05,
#         "stability": 0.10,
#     },
#     # 🚀 Chaotic Charismatic
#     "Star-Lord": {
#         "intensity": 0.35,
#         "warmth": 0.35,
#         "mystery": 0.15,
#         "control": 0.05,
#         "stability": 0.10,
#     },
# }

#     def assign_mcu(self, adjusted_traits: dict):

#         results = {}

#         for name, traits in adjusted_traits.items():

#             best_character = None
#             best_score = -1

#             for character, weights in self.MCU_MATRIX.items():

#                 score = 0

#                 for trait, weight in weights.items():
#                     score += traits.get(trait, 0) * weight

#                 if score > best_score:
#                     best_score = score
#                     best_character = character

#             results[name] = {"character": best_character, "score": round(best_score, 3)}

#         return results


class CharacterEngine:

    MCU_MATRIX = {
        # 🔥 Dominant + Strategic + Assertive
        "Iron Man": {
            "intensity": 0.45,
            "control": 0.40,
            "warmth": 0.05,
            "stability": 0.05,
            "mystery": 0.05,
        },
        # 🛡 Balanced Leader
        "Captain America": {
            "warmth": 0.40,
            "stability": 0.35,
            "control": 0.15,
            "intensity": 0.05,
            "mystery": 0.05,
        },
        # 🌀 Strategic + Manipulative
        "Loki": {
            "mystery": 0.50,
            "control": 0.30,
            "intensity": 0.15,
            "warmth": 0.025,
            "stability": 0.025,
        },
        # ⚡ Energetic + Loud
        "Thor": {
            "intensity": 0.55,
            "warmth": 0.25,
            "control": 0.10,
            "stability": 0.05,
            "mystery": 0.05,
        },
        # 🔮 Calculated + Calm Strategist
        "Doctor Strange": {
            "control": 0.45,
            "mystery": 0.35,
            "stability": 0.15,
            "intensity": 0.025,
            "warmth": 0.025,
        },
        # 🕷 Friendly + Playful
        "Spider-Man": {
            "warmth": 0.45,
            "intensity": 0.30,
            "stability": 0.10,
            "control": 0.075,
            "mystery": 0.075,
        },
        # 💥 Pure Intensity + Chaos
        "Hulk": {
            "intensity": 0.65,
            "control": 0.05,
            "warmth": 0.05,
            "stability": 0.10,
            "mystery": 0.15,
        },
        # 🕶 Silent + Tactical
        "Black Widow": {
            "mystery": 0.45,
            "stability": 0.35,
            "control": 0.10,
            "intensity": 0.05,
            "warmth": 0.05,
        },
        # 🧠 Stable + Analytical
        "Vision": {
            "stability": 0.55,
            "warmth": 0.20,
            "control": 0.10,
            "intensity": 0.075,
            "mystery": 0.075,
        },
        # 🛰 Master Planner
        "Nick Fury": {
            "control": 0.55,
            "mystery": 0.30,
            "stability": 0.10,
            "intensity": 0.025,
            "warmth": 0.025,
        },
        # 🌪 Emotionally Intense + Unpredictable
        "Scarlet Witch": {
            "intensity": 0.40,
            "mystery": 0.35,
            "warmth": 0.10,
            "control": 0.05,
            "stability": 0.10,
        },
        # 🚀 Chaotic Charismatic
        "Star-Lord": {
            "intensity": 0.35,
            "warmth": 0.35,
            "mystery": 0.15,
            "control": 0.05,
            "stability": 0.10,
        },
    }

    REQUIRED_TRAITS = ["intensity", "control", "warmth", "stability", "mystery"]

    def run(self, adjusted_traits: dict) -> dict:

        results = {}

        for name, traits in adjusted_traits.items():

            # Ensure all traits exist and are bounded
            safe_traits = {
                t: max(0, min(traits.get(t, 0), 1)) for t in self.REQUIRED_TRAITS
            }

            scores = []

            for character, weights in self.MCU_MATRIX.items():

                score = sum(
                    safe_traits[trait] * weight for trait, weight in weights.items()
                )

                scores.append((character, score))

            # Sort descending
            scores.sort(key=lambda x: x[1], reverse=True)

            best_character, best_score = scores[0]
            second_score = scores[1][1] if len(scores) > 1 else 0

            confidence = best_score - second_score

            results[name] = {
                "character": best_character,
                "score": round(best_score, 3),
                "confidence": round(confidence, 3),
            }

        return results
