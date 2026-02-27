import re
from datetime import datetime
from typing import Dict


class WhatsAppParser:

    ANDROID_PATTERN = re.compile(
        r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}\s?[ap]m)\s-\s(.*?):\s(.*)",
        re.IGNORECASE,
    )

    IOS_PATTERN = re.compile(
        r"^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}:\d{2}\s?[APMapm]{2})\]\s(.*?):\s(.*)"
    )

    SYSTEM_MESSAGE_KEYWORDS = [
        "added",
        "removed",
        "changed",
        "created group",
        "missed voice call",
        "video call",
        "joined using",
        "left",
        "security code",
        "encrypted",
    ]

    def parse(self, file_content: str) -> Dict:

        file_content = file_content.replace("\u202f", " ")
        file_content = file_content.replace("\u00a0", " ")

        lines = file_content.splitlines()

        messages = []
        participants = set()

        current_message = None
        skipped_lines = 0

        for line in lines:

            line = line.strip()
            if not line:
                continue

            android_match = self.ANDROID_PATTERN.match(line)
            ios_match = self.IOS_PATTERN.match(line)

            if android_match:
                parsed = self._extract(android_match)
            elif ios_match:
                parsed = self._extract(ios_match)
            else:
                if current_message:
                    current_message["text"] += "\n" + line
                continue

            if not parsed:
                skipped_lines += 1
                continue

            timestamp, sender, text = parsed

            # Skip system messages
            if self._is_system_message(text):
                continue

            current_message = {
                "timestamp": timestamp,
                "sender": sender,
                "text": text,
            }

            messages.append(current_message)
            participants.add(sender)

        return {
            "participants": sorted(list(participants)),
            "messages": messages,
            "meta": {
                "total_messages_parsed": len(messages),
                "skipped_lines": skipped_lines,
            },
        }

    def _extract(self, match):

        try:
            timestamp_str = f"{match.group(1)} {match.group(2)}"
            sender = match.group(3).strip()
            text = match.group(4).strip()

            timestamp = self._parse_datetime(timestamp_str)

            return timestamp, sender, text

        except Exception:
            return None

    def _parse_datetime(self, timestamp_str: str) -> datetime:

        for fmt in [
            "%d/%m/%y %I:%M %p",
            "%d/%m/%Y %I:%M %p",
            "%d/%m/%y %I:%M:%S %p",
            "%d/%m/%Y %I:%M:%S %p",
        ]:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue

        return None  # safer than raising error

    def _is_system_message(self, text: str) -> bool:
        lower = text.lower()
        return any(keyword in lower for keyword in self.SYSTEM_MESSAGE_KEYWORDS)


# import re
# from datetime import datetime
# from typing import Dict


# class WhatsAppParser:

#     # Flexible Android pattern
#     ANDROID_PATTERN = re.compile(
#         r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}\s?[ap]m)\s-\s(.*?):\s(.*)",
#         re.IGNORECASE,
#     )

#     # Flexible iOS pattern
#     IOS_PATTERN = re.compile(
#         r"^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}:\d{2}\s?[APMapm]{2})\]\s(.*?):\s(.*)"
#     )

#     def parse(self, file_content: str) -> Dict:
#         # 🔥 Normalize weird unicode spaces
#         file_content = file_content.replace("\u202f", " ")
#         file_content = file_content.replace("\u00a0", " ")

#         lines = file_content.splitlines()
#         messages = []
#         participants = set()

#         current_message = None

#         for line in lines:
#             line = line.strip()

#             android_match = self.ANDROID_PATTERN.match(line)
#             ios_match = self.IOS_PATTERN.match(line)

#             if android_match:
#                 timestamp_str = f"{android_match.group(1)} {android_match.group(2)}"
#                 sender = android_match.group(3).strip()
#                 text = android_match.group(4).strip()

#                 timestamp = self._parse_datetime(timestamp_str)

#                 current_message = {
#                     "timestamp": timestamp,
#                     "sender": sender,
#                     "text": text,
#                 }

#                 messages.append(current_message)
#                 participants.add(sender)

#             elif ios_match:
#                 timestamp_str = f"{ios_match.group(1)} {ios_match.group(2)}"
#                 sender = ios_match.group(3).strip()
#                 text = ios_match.group(4).strip()

#                 timestamp = self._parse_datetime(timestamp_str)

#                 current_message = {
#                     "timestamp": timestamp,
#                     "sender": sender,
#                     "text": text,
#                 }

#                 messages.append(current_message)
#                 participants.add(sender)

#             else:
#                 # Multi-line continuation
#                 if current_message:
#                     current_message["text"] += "\n" + line

#         return {"participants": list(participants), "messages": messages}

#     def _parse_datetime(self, timestamp_str: str) -> datetime:
#         for fmt in [
#             "%d/%m/%y %I:%M %p",
#             "%d/%m/%Y %I:%M %p",
#             "%d/%m/%y %I:%M:%S %p",
#             "%d/%m/%Y %I:%M:%S %p",
#         ]:
#             try:
#                 return datetime.strptime(timestamp_str, fmt)
#             except ValueError:
#                 continue

#         raise ValueError(f"Unknown datetime format: {timestamp_str}")
