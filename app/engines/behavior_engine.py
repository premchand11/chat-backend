class BehaviorEngine:

    def run(self, metrics: dict, traits: dict) -> dict:

        participants = metrics.get("participant_metrics", {})
        if not participants:
            return {}

        results = {}

        # --- Collect normalization vectors safely ---
        def collect(key, default=0):
            return [p.get(key, default) or 0 for p in participants.values()]

        shares = collect("message_share_ratio")
        reply_times = collect("median_reply_time")
        variances = collect("reply_time_variance")
        lengths = collect("avg_message_length")
        emojis = collect("emoji_density")
        questions = collect("question_ratio")
        nights = collect("night_activity_ratio")

        # --- Precompute min/max for efficiency ---
        def min_max(arr):
            return min(arr), max(arr)

        share_min, share_max = min_max(shares)
        reply_min, reply_max = min_max(reply_times)
        var_min, var_max = min_max(variances)
        len_min, len_max = min_max(lengths)
        emo_min, emo_max = min_max(emojis)
        ques_min, ques_max = min_max(questions)
        night_min, night_max = min_max(nights)

        def normalize(value, min_v, max_v):
            if max_v == min_v:
                return 0.5
            return (value - min_v) / (max_v - min_v)

        for name, m in participants.items():

            if name not in traits:
                continue

            control = traits[name].get("control", 0.5)
            warmth = traits[name].get("warmth", 0.5)

            share_norm = normalize(
                m.get("message_share_ratio", 0), share_min, share_max
            )
            reply_norm = 1 - normalize(
                m.get("median_reply_time", 0), reply_min, reply_max
            )
            variance_norm = normalize(m.get("reply_time_variance", 0), var_min, var_max)
            length_norm = normalize(m.get("avg_message_length", 0), len_min, len_max)
            emoji_norm = normalize(m.get("emoji_density", 0), emo_min, emo_max)
            question_norm = normalize(m.get("question_ratio", 0), ques_min, ques_max)
            night_norm = normalize(
                m.get("night_activity_ratio", 0), night_min, night_max
            )

            # 🔥 Emotional Investment
            investment = (
                0.30 * share_norm
                + 0.20 * reply_norm
                + 0.20 * question_norm
                + 0.15 * length_norm
                + 0.15 * night_norm
            )

            # 👑 Dominance
            dominance = 0.50 * share_norm + 0.30 * control + 0.20 * reply_norm

            # 👻 Ghosting
            ghost = (
                0.50 * (1 - reply_norm) + 0.30 * variance_norm + 0.20 * (1 - share_norm)
            )

            # 🧊 Dry Texting
            dry = (
                0.35 * (1 - emoji_norm)
                + 0.30 * (1 - question_norm)
                + 0.20 * (1 - length_norm)
                + 0.15 * (1 - warmth)
            )

            results[name] = {
                "investment": round(max(0, min(investment, 1)), 3),
                "dominance": round(max(0, min(dominance, 1)), 3),
                "ghost_score": round(max(0, min(ghost, 1)), 3),
                "dry_text_score": round(max(0, min(dry, 1)), 3),
            }

        return results


# class BehaviorEngine:

#     def compute(self, metrics: dict, traits: dict) -> dict:

#         participants = metrics["participant_metrics"]

#         results = {}

#         # collect normalization vectors
#         shares = [p["message_share_ratio"] for p in participants.values()]
#         reply_times = [p["median_reply_time"] or 0 for p in participants.values()]
#         variances = [p["reply_time_variance"] for p in participants.values()]
#         lengths = [p["avg_message_length"] for p in participants.values()]
#         emojis = [p["emoji_density"] for p in participants.values()]
#         questions = [p["question_ratio"] for p in participants.values()]
#         nights = [p["night_activity_ratio"] for p in participants.values()]

#         def normalize(value, arr):
#             min_v = min(arr)
#             max_v = max(arr)
#             if max_v == min_v:
#                 return 0.5
#             return (value - min_v) / (max_v - min_v)

#         for name, m in participants.items():
#             if name not in traits:
#                 continue

#             share_norm = normalize(m["message_share_ratio"], shares)
#             reply_norm = 1 - normalize(m["median_reply_time"] or 0, reply_times)
#             variance_norm = normalize(m["reply_time_variance"], variances)
#             length_norm = normalize(m["avg_message_length"], lengths)
#             emoji_norm = normalize(m["emoji_density"], emojis)
#             question_norm = normalize(m["question_ratio"], questions)
#             night_norm = normalize(m["night_activity_ratio"], nights)

#             # 🔥 Emotional Investment
#             investment = (
#                 0.30 * share_norm
#                 + 0.20 * reply_norm
#                 + 0.20 * question_norm
#                 + 0.15 * length_norm
#                 + 0.15 * night_norm
#             )

#             # 👑 Dominance
#             dominance = (
#                 0.50 * share_norm + 0.30 * traits[name]["control"] + 0.20 * reply_norm
#             )

#             # 👻 Ghosting
#             ghost = (
#                 0.50 * (1 - reply_norm) + 0.30 * variance_norm + 0.20 * (1 - share_norm)
#             )

#             # 🧊 Dry Texting
#             dry = (
#                 0.35 * (1 - emoji_norm)
#                 + 0.30 * (1 - question_norm)
#                 + 0.20 * (1 - length_norm)
#                 + 0.15 * (1 - traits[name]["warmth"])
#             )

#             results[name] = {
#                 "investment": round(investment, 3),
#                 "dominance": round(dominance, 3),
#                 "ghost_score": round(ghost, 3),
#                 "dry_text_score": round(dry, 3),
#             }

#         return results
