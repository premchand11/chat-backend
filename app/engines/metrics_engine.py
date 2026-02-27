from collections import defaultdict
from typing import Dict
import statistics
import re


class MetricsEngine:

    EMOJI_PATTERN = re.compile(
        "[\U0001f600-\U0001f64f"
        "\U0001f300-\U0001f5ff"
        "\U0001f680-\U0001f6ff"
        "\U0001f1e0-\U0001f1ff]+",
        flags=re.UNICODE,
    )

    def run(self, parsed_data: Dict) -> Dict:

        messages = parsed_data.get("messages", [])
        if not messages:
            return {
                "participant_metrics": {},
                "chat_metrics": {"total_messages": 0, "time_span_days": 0},
            }

        # Safe sort
        messages = sorted(messages, key=lambda x: x.get("timestamp"))

        participant_metrics = defaultdict(self._default_metrics)

        total_messages = len(messages)
        previous_message = None

        for msg in messages:

            sender = msg.get("sender")
            text = msg.get("text", "")
            timestamp = msg.get("timestamp")

            if not sender or not timestamp:
                continue

            metrics = participant_metrics[sender]

            # ---- Basic counts ----
            metrics["message_count"] += 1
            metrics["total_characters"] += len(text)
            metrics["total_words"] += len(text.split())

            emojis = self.EMOJI_PATTERN.findall(text)
            metrics["emoji_count"] += len(emojis)

            metrics["question_count"] += text.count("?")
            metrics["exclamation_count"] += text.count("!")
            metrics["uppercase_characters"] += sum(1 for c in text if c.isupper())

            # ---- Night activity (10PM–4AM) ----
            hour = timestamp.hour
            if 22 <= hour or hour <= 4:
                metrics["night_messages"] += 1

            # ---- First & Last Message ----
            if metrics["first_message_time"] is None:
                metrics["first_message_time"] = timestamp

            metrics["last_message_time"] = timestamp

            # ---- Reply delay modeling ----
            if previous_message:
                prev_sender = previous_message.get("sender")
                prev_timestamp = previous_message.get("timestamp")

                if prev_sender != sender and prev_timestamp:
                    delay = (timestamp - prev_timestamp).total_seconds()

                    if 5 <= delay < 86400:
                        metrics["reply_delays"].append(delay)

            previous_message = msg

        # ---- Derived metrics ----
        for sender, metrics in participant_metrics.items():

            mc = metrics["message_count"]

            if mc > 0:
                metrics["question_ratio"] = self._clamp(metrics["question_count"] / mc)
                metrics["exclamation_ratio"] = self._clamp(
                    metrics["exclamation_count"] / mc
                )
                metrics["avg_message_length"] = metrics["total_characters"] / mc
                metrics["emoji_density"] = self._clamp(metrics["emoji_count"] / mc)
                metrics["night_activity_ratio"] = self._clamp(
                    metrics["night_messages"] / mc
                )
            else:
                metrics["question_ratio"] = 0
                metrics["exclamation_ratio"] = 0
                metrics["avg_message_length"] = 0
                metrics["emoji_density"] = 0
                metrics["night_activity_ratio"] = 0

            # ---- Reply metrics ----
            delays = metrics["reply_delays"]

            if delays:
                metrics["median_reply_time"] = statistics.median(delays)
                metrics["reply_time_variance"] = (
                    statistics.pvariance(delays) if len(delays) > 1 else 0
                )
            else:
                metrics["median_reply_time"] = None
                metrics["reply_time_variance"] = 0

        # ---- Message share ratio ----
        for sender, metrics in participant_metrics.items():
            metrics["message_share_ratio"] = (
                metrics["message_count"] / total_messages if total_messages > 0 else 0
            )

        # ---- Chat-level metrics ----
        time_span_days = 0
        if len(messages) > 1:
            first = messages[0].get("timestamp")
            last = messages[-1].get("timestamp")

            if first and last:
                time_span_days = (last - first).days

        return {
            "participant_metrics": dict(participant_metrics),
            "chat_metrics": {
                "total_messages": total_messages,
                "time_span_days": time_span_days,
            },
        }

    def _default_metrics(self):
        return {
            "message_count": 0,
            "total_characters": 0,
            "total_words": 0,
            "emoji_count": 0,
            "question_count": 0,
            "exclamation_count": 0,
            "uppercase_characters": 0,
            "reply_delays": [],
            "first_message_time": None,
            "last_message_time": None,
            "night_messages": 0,
        }

    def _clamp(self, value: float) -> float:
        return max(0.0, min(value, 1.0))


# from collections import defaultdict
# from typing import Dict
# import statistics
# import re


# class MetricsEngine:

#     EMOJI_PATTERN = re.compile(
#         "[\U0001f600-\U0001f64f"  # emoticons
#         "\U0001f300-\U0001f5ff"  # symbols
#         "\U0001f680-\U0001f6ff"  # transport
#         "\U0001f1e0-\U0001f1ff]+",  # flags
#         flags=re.UNICODE,
#     )

#     def compute(self, parsed_data: Dict) -> Dict:

#         messages = sorted(parsed_data["messages"], key=lambda x: x["timestamp"])

#         participant_metrics = defaultdict(
#             lambda: {
#                 "message_count": 0,
#                 "total_characters": 0,
#                 "total_words": 0,
#                 "emoji_count": 0,
#                 "question_count": 0,
#                 "exclamation_count": 0,
#                 "uppercase_characters": 0,
#                 "reply_delays": [],
#                 "first_message_time": None,
#                 "last_message_time": None,
#                 "night_messages": 0,
#             }
#         )

#         total_messages = len(messages)
#         previous_message = None

#         # 🔥 MAIN LOOP
#         for msg in messages:
#             sender = msg["sender"]
#             text = msg["text"]
#             timestamp = msg["timestamp"]

#             metrics = participant_metrics[sender]

#             # Basic counts
#             metrics["message_count"] += 1
#             metrics["total_characters"] += len(text)
#             metrics["total_words"] += len(text.split())

#             # Emoji count
#             emojis = self.EMOJI_PATTERN.findall(text)
#             metrics["emoji_count"] += len(emojis)

#             # Question / exclamation
#             metrics["question_count"] += text.count("?")
#             metrics["exclamation_count"] += text.count("!")

#             # Uppercase detection
#             metrics["uppercase_characters"] += sum(1 for c in text if c.isupper())

#             # Night activity (10PM–4AM)
#             if 22 <= timestamp.hour or timestamp.hour <= 4:
#                 metrics["night_messages"] += 1

#             # First & last timestamps
#             if metrics["first_message_time"] is None:
#                 metrics["first_message_time"] = timestamp

#             metrics["last_message_time"] = timestamp

#             # 🔥 Reply logic (ignore <5s and >24h)
#             if previous_message and previous_message["sender"] != sender:
#                 delay = (timestamp - previous_message["timestamp"]).total_seconds()

#                 if 5 <= delay < 86400:
#                     metrics["reply_delays"].append(delay)

#             previous_message = msg

#         # 🔥 DERIVED METRICS
#         for sender, metrics in participant_metrics.items():

#             # Ratios
#             if metrics["message_count"] > 0:
#                 metrics["question_ratio"] = (
#                     metrics["question_count"] / metrics["message_count"]
#                 )
#                 metrics["exclamation_ratio"] = (
#                     metrics["exclamation_count"] / metrics["message_count"]
#                 )
#                 metrics["avg_message_length"] = (
#                     metrics["total_characters"] / metrics["message_count"]
#                 )
#                 metrics["emoji_density"] = (
#                     metrics["emoji_count"] / metrics["message_count"]
#                 )
#                 metrics["night_activity_ratio"] = (
#                     metrics["night_messages"] / metrics["message_count"]
#                 )
#             else:
#                 metrics["question_ratio"] = 0
#                 metrics["exclamation_ratio"] = 0
#                 metrics["avg_message_length"] = 0
#                 metrics["emoji_density"] = 0
#                 metrics["night_activity_ratio"] = 0

#             # Reply metrics
#             if metrics["reply_delays"]:
#                 metrics["median_reply_time"] = statistics.median(
#                     metrics["reply_delays"]
#                 )
#                 metrics["reply_time_variance"] = (
#                     statistics.variance(metrics["reply_delays"])
#                     if len(metrics["reply_delays"]) > 1
#                     else 0
#                 )
#             else:
#                 metrics["median_reply_time"] = None
#                 metrics["reply_time_variance"] = 0

#         # Message share ratio
#         for sender, metrics in participant_metrics.items():
#             metrics["message_share_ratio"] = (
#                 metrics["message_count"] / total_messages if total_messages > 0 else 0
#             )

#         # Chat-level metrics
#         time_span_days = 0
#         if messages:
#             time_span_days = (messages[-1]["timestamp"] - messages[0]["timestamp"]).days

#         return {
#             "participant_metrics": dict(participant_metrics),
#             "chat_metrics": {
#                 "total_messages": total_messages,
#                 "time_span_days": time_span_days,
#             },
#         }
