class ExplanationEngine:

    CHARACTER_PRIMARY_BIAS = {
        "Iron Man": "control",
        "Black Widow": "mystery",
        "Spider-Man": "warmth",
        "Hulk": "intensity",
        "Vision": "stability",
        "Loki": "mystery",
    }

    TRAIT_LINES = {
        "intensity": {
            "high": "Your emotional intensity dominates the rhythm of conversations.",
            "medium": "You inject strong momentum into discussions.",
            "soft": "You bring bursts of energy when needed.",
        },
        "warmth": {
            "high": "People instinctively feel comfortable opening up around you.",
            "medium": "Your presence makes conversations feel more human.",
            "soft": "You add warmth without overpowering others.",
        },
        "control": {
            "high": "You steer conversations decisively and confidently.",
            "medium": "You influence direction without being obvious about it.",
            "soft": "You occasionally guide the flow of discussion.",
        },
        "stability": {
            "high": "Your consistency makes you one of the most grounded presences here.",
            "medium": "You remain steady even when conversations shift.",
            "soft": "You keep things from spiraling when chaos appears.",
        },
        "mystery": {
            "high": "There’s a depth to you that others can’t fully decode.",
            "medium": "You don’t reveal everything — and that works in your favor.",
            "soft": "You maintain a subtle unpredictability.",
        },
    }

    def run(
        self,
        name: str,
        traits: dict,
        character: str,
        confidence: float = 0.0,
    ) -> str:

        if not traits:
            return f"{name}, not enough data to generate an explanation."

        # Clamp traits safely between 0–1
        safe_traits = {k: max(0.0, min(float(v), 1.0)) for k, v in traits.items()}

        if not safe_traits:
            return f"{name}, not enough data to generate an explanation."

        sorted_traits = sorted(
            safe_traits.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        primary_trait = sorted_traits[0][0]
        secondary_trait = (
            sorted_traits[1][0] if len(sorted_traits) > 1 else primary_trait
        )

        # Apply character bias
        bias_trait = self.CHARACTER_PRIMARY_BIAS.get(character)
        if bias_trait:
            primary_trait = bias_trait

        intro = self._character_intro(character, confidence)

        primary_value = safe_traits.get(primary_trait, 0.0)
        secondary_value = safe_traits.get(secondary_trait, 0.0)

        primary_line = self._trait_line(primary_trait, primary_value)
        secondary_line = self._trait_line(secondary_trait, secondary_value)
        group_line = self._group_behavior_line(safe_traits)

        return (
            f"{name}: {intro}\n\n"
            f"{primary_line}\n"
            f"{secondary_line}\n\n"
            f"{group_line}"
        )

    def _character_intro(self, character: str, confidence: float) -> str:

        intros = {
            "Iron Man": "You’re the strategist who doesn’t wait for permission.",
            "Captain America": "You lead with integrity and emotional strength.",
            "Loki": "You move in silence, but your presence shifts everything.",
            "Thor": "You enter loud, bold, and impossible to ignore.",
            "Doctor Strange": "You think three moves ahead before anyone notices.",
            "Spider-Man": "You bring energy, humor, and heart into every interaction.",
            "Hulk": "When you show up, the emotional temperature changes instantly.",
            "Black Widow": "You observe quietly — but nothing escapes you.",
            "Vision": "You operate with calm precision and steady presence.",
            "Nick Fury": "You don’t need attention — you control outcomes.",
            "Scarlet Witch": "You carry intensity beneath the surface.",
            "Star-Lord": "You balance chaos with charisma effortlessly.",
        }

        base = intros.get(character, f"As {character}, you bring a distinct energy.")

        if confidence < 0.05:
            return base + " Your personality shows a balanced mix of traits."
        if confidence < 0.15:
            return base + " You share strong similarities with this archetype."
        return base

    def _trait_line(self, trait: str, value: float) -> str:

        if value >= 0.75:
            level = "high"
        elif value >= 0.55:
            level = "medium"
        else:
            level = "soft"

        trait_lines = self.TRAIT_LINES.get(
            trait,
            {
                "high": "Your presence is strongly felt.",
                "medium": "You influence the conversation noticeably.",
                "soft": "You contribute in subtle ways.",
            },
        )

        return trait_lines[level]

    def _group_behavior_line(self, traits: dict) -> str:

        control = traits.get("control", 0.0)
        warmth = traits.get("warmth", 0.0)
        mystery = traits.get("mystery", 0.0)
        stability = traits.get("stability", 0.0)
        intensity = traits.get("intensity", 0.0)

        if control >= 0.85:
            return "In this group, you clearly set the tone."
        if warmth >= 0.85:
            return "You’re the emotional glue that holds interactions together."
        if mystery >= 0.85:
            return "Even when silent, people feel your presence."
        if stability >= 0.85:
            return "You’re the calm center when things get unpredictable."
        if intensity >= 0.85:
            return "Your energy alone can shift the group dynamic."

        return "You shape the group dynamic more than you probably realize."


# class ExplanationEngine:

#     def generate(self, name: str, traits: dict, character: str) -> str:
#         if not traits:
#             return f"{name}, not enough data to generate an explanation."

#         sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
#         primary_trait = sorted_traits[0][0]

#         # Character bias
#         if character == "Iron Man" and primary_trait != "control":
#             primary_trait = "control"

#         if character == "Black Widow" and primary_trait != "mystery":
#             primary_trait = "mystery"

#         if character == "Spider-Man" and primary_trait != "warmth":
#             primary_trait = "warmth"

#         if character == "Hulk" and primary_trait != "intensity":
#             primary_trait = "intensity"

#         if character == "Vision" and primary_trait != "stability":
#             primary_trait = "stability"

#         if character == "Loki" and primary_trait != "mystery":
#             primary_trait = "mystery"

#         secondary_trait = (
#             sorted_traits[1][0] if len(sorted_traits) > 1 else primary_trait
#         )

#         intro = self._character_intro(character)
#         primary_value = traits.get(primary_trait, 0.0)
#         secondary_value = traits.get(secondary_trait, 0.0)

#         primary_line = self._trait_line(primary_trait, True, primary_value)
#         secondary_line = self._trait_line(secondary_trait, False, secondary_value)
#         group_line = self._group_behavior_line(traits)

#         return f"{name}: {intro}\n{primary_line}\n{secondary_line}\n{group_line}"

#     # 🔥 Cinematic character intros
#     def _character_intro(self, character: str) -> str:

#         intros = {
#             "Iron Man": "You’re the strategist who doesn’t wait for permission.",
#             "Captain America": "You lead with integrity and emotional strength.",
#             "Loki": "You move in silence, but your presence shifts everything.",
#             "Thor": "You enter loud, bold, and impossible to ignore.",
#             "Doctor Strange": "You think three moves ahead before anyone notices.",
#             "Spider-Man": "You bring energy, humor, and heart into every interaction.",
#             "Hulk": "When you show up, the emotional temperature changes instantly.",
#             "Black Widow": "You observe quietly — but nothing escapes you.",
#             "Vision": "You operate with calm precision and steady presence.",
#             "Nick Fury": "You don’t need attention — you control outcomes.",
#             "Scarlet Witch": "You carry intensity beneath the surface.",
#             "Star-Lord": "You balance chaos with charisma effortlessly.",
#         }

#         return intros.get(character, f"As {character}, you bring a distinct energy.")

#     # 🔥 Trait-based lines with strength variation
#     def _trait_line(self, trait: str, strong: bool, value: float) -> str:

#         high = value > 0.8
#         medium = 0.6 < value <= 0.8

#         lines = {
#             "intensity": {
#                 "high": "Your emotional intensity dominates the rhythm of conversations.",
#                 "medium": "You inject strong momentum into discussions.",
#                 "soft": "You bring bursts of energy when needed.",
#             },
#             "warmth": {
#                 "high": "People instinctively feel comfortable opening up around you.",
#                 "medium": "Your presence makes conversations feel more human.",
#                 "soft": "You add warmth without overpowering others.",
#             },
#             "control": {
#                 "high": "You steer conversations decisively and confidently.",
#                 "medium": "You influence direction without being obvious about it.",
#                 "soft": "You occasionally guide the flow of discussion.",
#             },
#             "stability": {
#                 "high": "Your consistency makes you one of the most grounded presences here.",
#                 "medium": "You remain steady even when conversations shift.",
#                 "soft": "You keep things from spiraling when chaos appears.",
#             },
#             "mystery": {
#                 "high": "There’s a depth to you that others can’t fully decode.",
#                 "medium": "You don’t reveal everything — and that works in your favor.",
#                 "soft": "You maintain a subtle unpredictability.",
#             },
#         }

#         trait_lines = lines.get(
#             trait,
#             {
#                 "high": "Your presence is strongly felt.",
#                 "medium": "You influence the conversation.",
#                 "soft": "You contribute in subtle ways.",
#             },
#         )

#         if high:
#             return trait_lines["high"]
#         if medium:
#             return trait_lines["medium"]
#         return trait_lines["soft"]

#     # 🔥 Group behavior interpretation
#     def _group_behavior_line(self, traits: dict) -> str:
#         control = traits.get("control", 0.0)
#         warmth = traits.get("warmth", 0.0)
#         mystery = traits.get("mystery", 0.0)
#         stability = traits.get("stability", 0.0)
#         intensity = traits.get("intensity", 0.0)

#         if control > 0.85:
#             return "In this group, you clearly set the tone."
#         if warmth > 0.85:
#             return "You’re the emotional glue that holds interactions together."
#         if mystery > 0.85:
#             return "Even when silent, people feel your presence."
#         if stability > 0.85:
#             return "You’re the calm center when things get unpredictable."
#         if intensity > 0.85:
#             return "Your energy alone can shift the group dynamic."

#         return "You shape the group dynamic more than you probably realize."
