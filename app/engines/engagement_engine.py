from collections import defaultdict
from datetime import timedelta


class EngagementEngine:

    def run(
        self,
        parsed_data: dict,
        reply_window_minutes: int = 20,
        forward_message_check: int = 8,
    ) -> dict:

        messages = parsed_data.get("messages", [])
        if not messages:
            return {}

        # Sort safely
        messages = sorted(messages, key=lambda x: x.get("timestamp"))

        ignored_count = defaultdict(int)
        total_messages = defaultdict(int)

        reply_window = timedelta(minutes=reply_window_minutes)

        participants = set(msg.get("sender") for msg in messages)
        group_size = len(participants)

        # Dynamic threshold
        required_other_speakers = 1 if group_size <= 2 else 2

        for i in range(len(messages)):

            current = messages[i]
            sender = current.get("sender")
            timestamp = current.get("timestamp")

            if not sender or not timestamp:
                continue

            total_messages[sender] += 1

            # Skip last message (can't evaluate reply)
            if i == len(messages) - 1:
                continue

            window_end = timestamp + reply_window
            replied = False

            j = i + 1

            while j < len(messages) and messages[j].get("timestamp") <= window_end:
                if messages[j].get("sender") != sender:
                    replied = True
                    break
                j += 1

            if replied:
                continue

            forward_messages = messages[i + 1 : i + 1 + forward_message_check]

            if len(forward_messages) < 3:
                continue

            other_speakers = {
                msg.get("sender")
                for msg in forward_messages
                if msg.get("sender") != sender
            }

            if len(other_speakers) >= required_other_speakers:
                ignored_count[sender] += 1

        results = {}

        for person, total in total_messages.items():
            ignored = ignored_count[person]
            ignored_ratio = ignored / total if total > 0 else 0

            results[person] = {
                "ignored_count": ignored,
                "ignored_ratio": round(min(max(ignored_ratio, 0), 1), 3),
            }

        return results


# from collections import defaultdict
# from datetime import timedelta


# class EngagementEngine:

#     def compute_ignored(
#         self,
#         parsed_data: dict,
#         reply_window_minutes=20,
#         forward_message_check=8,
#     ):

#         messages = sorted(parsed_data["messages"], key=lambda x: x["timestamp"])

#         ignored_count = defaultdict(int)
#         total_messages = defaultdict(int)

#         reply_window = timedelta(minutes=reply_window_minutes)

#         for i in range(len(messages) - 1):

#             current = messages[i]
#             sender = current["sender"]
#             total_messages[sender] += 1

#             # ---- Step 1: Check direct reply window ----
#             window_end = current["timestamp"] + reply_window
#             replied = False

#             j = i + 1
#             while j < len(messages) and messages[j]["timestamp"] <= window_end:
#                 if messages[j]["sender"] != sender:
#                     replied = True
#                     break
#                 j += 1

#             if replied:
#                 continue

#             # ---- Step 2: Check forward movement ----
#             forward_messages = messages[i + 1 : i + 1 + forward_message_check]

#             if len(forward_messages) < 3:
#                 continue  # Not enough activity to judge

#             other_speakers = set()
#             for msg in forward_messages:
#                 if msg["sender"] != sender:
#                     other_speakers.add(msg["sender"])

#             # If 2+ others talked and sender didn't re-enter → ignored
#             if len(other_speakers) >= 2:
#                 ignored_count[sender] += 1

#         results = {}

#         for person in total_messages:
#             total = total_messages[person]
#             ignored = ignored_count[person]

#             ignored_ratio = ignored / total if total > 0 else 0

#             results[person] = {
#                 "ignored_count": ignored,
#                 "ignored_ratio": round(ignored_ratio, 3),
#             }

#         return results
