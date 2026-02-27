from typing import Dict


class TraitEngine:

    BOT_NAMES = {"meta ai", "ai", "bot"}

    REQUIRED_KEYS = [
        "avg_message_length",
        "emoji_density",
        "message_share_ratio",
        "median_reply_time",
        "reply_time_variance",
        "night_activity_ratio",
        "question_ratio",
        "exclamation_ratio",
    ]

    def run(self, metrics: Dict) -> Dict:

        participants = metrics.get("participant_metrics", {})

        # Filter bots/system names
        participants = {
            name: data
            for name, data in participants.items()
            if name.lower() not in self.BOT_NAMES
        }

        if not participants:
            return {}

        # Collect normalization vectors safely
        vectors = {key: [] for key in self.REQUIRED_KEYS}

        for data in participants.values():
            for key in self.REQUIRED_KEYS:
                value = data.get(key, 0) or 0
                vectors[key].append(value)

        # Precompute min/max bounds
        bounds = {key: (min(values), max(values)) for key, values in vectors.items()}

        def normalize(value, key):
            min_v, max_v = bounds[key]
            if max_v == min_v:
                return 0.5
            return (value - min_v) / (max_v - min_v)

        trait_results = {}

        for name, data in participants.items():

            length_norm = normalize(
                data.get("avg_message_length", 0), "avg_message_length"
            )
            emoji_norm = normalize(data.get("emoji_density", 0), "emoji_density")
            share_norm = normalize(
                data.get("message_share_ratio", 0), "message_share_ratio"
            )
            reply_norm = 1 - normalize(
                data.get("median_reply_time", 0) or 0, "median_reply_time"
            )
            variance_norm = 1 - normalize(
                data.get("reply_time_variance", 0), "reply_time_variance"
            )
            night_norm = normalize(
                data.get("night_activity_ratio", 0), "night_activity_ratio"
            )
            question_norm = normalize(data.get("question_ratio", 0), "question_ratio")
            exclaim_norm = normalize(
                data.get("exclamation_ratio", 0), "exclamation_ratio"
            )

            # 🔥 INTENSITY
            intensity = 0.4 * length_norm + 0.3 * emoji_norm + 0.3 * share_norm

            # 💗 WARMTH
            warmth = (
                0.30 * emoji_norm
                + 0.25 * question_norm
                + 0.20 * exclaim_norm
                + 0.15 * reply_norm
                + 0.10 * (1 - abs(share_norm - 0.5) * 2)
            )

            # 👑 CONTROL
            control = share_norm

            # 🧊 STABILITY
            stability = 0.6 * variance_norm + 0.4 * reply_norm

            # 👻 MYSTERY
            mystery = 0.6 * (1 - share_norm) + 0.4 * night_norm

            trait_results[name] = {
                "intensity": round(self._clamp(intensity), 3),
                "warmth": round(self._clamp(warmth), 3),
                "control": round(self._clamp(control), 3),
                "stability": round(self._clamp(stability), 3),
                "mystery": round(self._clamp(mystery), 3),
            }

        return trait_results

    def _clamp(self, value: float) -> float:
        return max(0.0, min(value, 1.0))


# from typing import Dict


# class TraitEngine:

#     def compute_traits(self, metrics: Dict) -> Dict:
#         participants = metrics.get("participant_metrics", {})

#         # Filter bots/system names
#         participants = {
#             name: data
#             for name, data in participants.items()
#             if name.lower() not in {"meta ai", "ai", "bot"}
#         }

#         if not participants:
#             return {}

#         # Collect normalization vectors
#         message_lengths = []
#         emoji_densities = []
#         message_shares = []
#         reply_times = []
#         reply_variances = []
#         night_ratios = []
#         question_ratios = []
#         exclamation_ratios = []

#         for data in participants.values():
#             message_lengths.append(data["avg_message_length"])
#             emoji_densities.append(data["emoji_density"])
#             message_shares.append(data["message_share_ratio"])
#             reply_times.append(data["median_reply_time"] or 0)
#             reply_variances.append(data["reply_time_variance"])
#             night_ratios.append(data["night_activity_ratio"])
#             question_ratios.append(data["question_ratio"])
#             exclamation_ratios.append(data["exclamation_ratio"])

#         # Min-max normalization helper
#         def normalize(value, values):
#             min_v = min(values)
#             max_v = max(values)
#             if max_v == min_v:
#                 return 0.5
#             return (value - min_v) / (max_v - min_v)

#         trait_results = {}

#         for name, data in participants.items():

#             length_norm = normalize(data["avg_message_length"], message_lengths)
#             emoji_norm = normalize(data["emoji_density"], emoji_densities)
#             share_norm = normalize(data["message_share_ratio"], message_shares)
#             reply_norm = 1 - normalize(data["median_reply_time"] or 0, reply_times)
#             variance_norm = 1 - normalize(data["reply_time_variance"], reply_variances)
#             night_norm = normalize(data["night_activity_ratio"], night_ratios)
#             question_norm = normalize(data["question_ratio"], question_ratios)
#             exclaim_norm = normalize(data["exclamation_ratio"], exclamation_ratios)

#             # 🔥 INTENSITY
#             intensity = 0.4 * length_norm + 0.3 * emoji_norm + 0.3 * share_norm

#             # 💗 WARMTH (Upgraded Behavioral Model)
#             warmth = (
#                 0.30 * emoji_norm
#                 + 0.25 * question_norm
#                 + 0.20 * exclaim_norm
#                 + 0.15 * reply_norm
#                 + 0.10 * (1 - abs(share_norm - 0.5) * 2)
#             )

#             # 👑 CONTROL (dominance via message share)
#             control = share_norm

#             # 🧊 STABILITY (consistent timing + responsiveness)
#             stability = 0.6 * variance_norm + 0.4 * reply_norm

#             # 👻 MYSTERY (low share + night presence)
#             mystery = 0.6 * (1 - share_norm) + 0.4 * night_norm

#             trait_results[name] = {
#                 "intensity": round(intensity, 3),
#                 "warmth": round(warmth, 3),
#                 "control": round(control, 3),
#                 "stability": round(stability, 3),
#                 "mystery": round(mystery, 3),
#             }

#         return trait_results
