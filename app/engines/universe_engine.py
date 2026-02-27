class UniverseEngine:

    UNIVERSE_WEIGHTS = {
        "mcu": {
            "intensity": 1.2,
            "warmth": 0.9,
            "control": 1.1,
            "stability": 1.0,
            "mystery": 1.0,
        },
        "harry_potter": {
            "intensity": 1.0,
            "warmth": 1.1,
            "control": 1.0,
            "stability": 1.0,
            "mystery": 1.2,
        },
        "animals": {
            "intensity": 1.0,
            "warmth": 1.2,
            "control": 0.9,
            "stability": 1.1,
            "mystery": 1.0,
        },
        "dc": {
            "intensity": 1.2,
            "warmth": 0.9,
            "control": 1.2,
            "stability": 1.0,
            "mystery": 1.1,
        },
        "mythology": {
            "intensity": 1.1,
            "warmth": 1.0,
            "control": 1.2,
            "stability": 1.0,
            "mystery": 1.2,
        },
    }

    def run(self, traits: dict, universe: str = "mcu") -> dict:

        if not traits:
            return {}

        weights = self.UNIVERSE_WEIGHTS.get(
            universe, self.UNIVERSE_WEIGHTS["mcu"]  # safe fallback
        )

        adjusted = {}

        for name, data in traits.items():

            adjusted[name] = {}

            for trait, value in data.items():

                weight = weights.get(trait, 1.0)

                new_value = value * weight

                # Clamp to 0–1
                adjusted[name][trait] = round(self._clamp(new_value), 3)

        return adjusted

    def _clamp(self, value: float) -> float:
        return max(0.0, min(value, 1.0))


# class UniverseEngine:

#     UNIVERSE_WEIGHTS = {
#         "mcu": {
#             "intensity": 1.2,
#             "warmth": 0.9,
#             "control": 1.1,
#             "stability": 1.0,
#             "mystery": 1.0,
#         },
#         "harry_potter": {
#             "intensity": 1.0,
#             "warmth": 1.1,
#             "control": 1.0,
#             "stability": 1.0,
#             "mystery": 1.2,
#         },
#         "animals": {
#             "intensity": 1.0,
#             "warmth": 1.2,
#             "control": 0.9,
#             "stability": 1.1,
#             "mystery": 1.0,
#         },
#         "dc": {
#             "intensity": 1.2,
#             "warmth": 0.9,
#             "control": 1.2,
#             "stability": 1.0,
#             "mystery": 1.1,
#         },
#         "mythology": {
#             "intensity": 1.1,
#             "warmth": 1.0,
#             "control": 1.2,
#             "stability": 1.0,
#             "mystery": 1.2,
#         },
#     }

#     def adjust(self, traits: dict, universe: str) -> dict:

#         weights = self.UNIVERSE_WEIGHTS.get(universe, {})

#         adjusted = {}

#         for name, data in traits.items():

#             adjusted[name] = {}

#             for trait, value in data.items():

#                 weight = weights.get(trait, 1.0)
#                 adjusted[name][trait] = round(value * weight, 3)

#         return adjusted
