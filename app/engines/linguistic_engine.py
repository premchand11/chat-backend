from collections import Counter, defaultdict
import re


class LinguisticEngine:

    STOPWORDS = {
        # English
        "the",
        "is",
        "in",
        "at",
        "to",
        "a",
        "and",
        "of",
        "for",
        "on",
        "it",
        "this",
        "that",
        "i",
        "you",
        "me",
        "we",
        "us",
        "are",
        "was",
        "were",
        "be",
        "been",
        "have",
        "has",
        "had",
        "do",
        "did",
        "does",
        "but",
        "if",
        "so",
        "with",
        "as",
        "an",
        "or",
        "from",
        "by",
        # Hinglish
        "hai",
        "hn",
        "na",
        "u",
        "he",
        "bhi",
        "toh",
        "bhai",
        "nhi",
        "nahi",
        "mai",
        "main",
        "aur",
        "ok",
    }

    SYSTEM_WORDS = {
        "media",
        "omitted",
        "message",
        "deleted",
        "sticker",
        "image",
        "video",
        "audio",
        "gif",
        "document",
        "edited",
    }

    EMOJI_PATTERN = re.compile(
        r"[\U0001f600-\U0001f64f"
        r"\U0001f300-\U0001f5ff"
        r"\U0001f680-\U0001f6ff"
        r"\U0001f1e0-\U0001f1ff]"
    )

    WORD_PATTERN = re.compile(r"\b[a-zA-Z']+\b")

    def run(self, parsed_data: dict) -> dict:

        messages = parsed_data.get("messages", [])
        if not messages:
            return {"participants": {}, "group": {}, "signatures": {}}

        participant_words = defaultdict(list)
        participant_emojis = defaultdict(list)

        group_words = []
        group_emojis = []

        # ---- Single pass over messages ----
        for msg in messages:
            sender = msg.get("sender", "Unknown")
            text = msg.get("text", "").lower()

            words = self._extract_words(text)
            emojis = self.EMOJI_PATTERN.findall(text)

            participant_words[sender].extend(words)
            participant_emojis[sender].extend(emojis)

            group_words.extend(words)
            group_emojis.extend(emojis)

        results = {"participants": {}, "group": {}, "signatures": {}}

        # ---- Participant stats ----
        for sender, words in participant_words.items():

            word_counter = Counter(words)
            emoji_counter = Counter(participant_emojis[sender])

            vocab_size = len(set(words))
            total_words = len(words)
            unique_ratio = vocab_size / total_words if total_words else 0

            results["participants"][sender] = {
                "top_words": word_counter.most_common(10),
                "top_emojis": emoji_counter.most_common(10),
                "vocabulary_size": vocab_size,
                "unique_word_ratio": round(unique_ratio, 3),
            }

        # ---- Group stats ----
        group_word_counter = Counter(group_words)
        group_emoji_counter = Counter(group_emojis)

        results["group"] = {
            "top_words": group_word_counter.most_common(15),
            "top_emojis": group_emoji_counter.most_common(15),
            "total_unique_words": len(set(group_words)),
        }

        # ---- Signature detection ----
        results["signatures"] = self._compute_signatures(
            participant_words, group_word_counter
        )

        return results

    def _extract_words(self, text: str):
        words = self.WORD_PATTERN.findall(text)
        return [
            w
            for w in words
            if len(w) > 2 and w not in self.STOPWORDS and w not in self.SYSTEM_WORDS
        ]

    def _compute_signatures(self, participant_words, group_word_counter):

        signature_results = {}

        for sender, words in participant_words.items():

            personal_counter = Counter(words)
            total_user_words = len(words)

            if total_user_words == 0:
                signature_results[sender] = []
                continue

            dynamic_threshold = max(5, int(0.01 * total_user_words))

            signatures = []

            for word, count in personal_counter.items():

                if count >= dynamic_threshold:
                    group_count = group_word_counter.get(word, 0)

                    if group_count > 0:
                        ratio = count / group_count

                        if ratio > 0.25:
                            signatures.append((word, round(min(ratio, 1), 2)))

            signatures.sort(key=lambda x: x[1], reverse=True)
            signature_results[sender] = signatures[:5]

        return signature_results


# from collections import Counter, defaultdict
# import re


# class LinguisticEngine:
#     STOPWORDS = {
#         # English
#         "the",
#         "is",
#         "in",
#         "at",
#         "to",
#         "a",
#         "and",
#         "of",
#         "for",
#         "on",
#         "it",
#         "this",
#         "that",
#         "i",
#         "you",
#         "me",
#         "we",
#         "us",
#         "are",
#         "was",
#         "were",
#         "be",
#         "been",
#         "have",
#         "has",
#         "had",
#         "do",
#         "did",
#         "does",
#         "but",
#         "if",
#         "so",
#         "with",
#         "as",
#         "an",
#         "or",
#         "from",
#         "by",
#         # Hinglish
#         "hai",
#         "hn",
#         "na",
#         "u",
#         "he",
#         "bhi",
#         "toh",
#         "bhai",
#         "nhi",
#         "nahi",
#         "mai",
#         "main",
#         "aur",
#         "ok",
#     }

#     SYSTEM_WORDS = {
#         "media",
#         "omitted",
#         "message",
#         "deleted",
#         "sticker",
#         "image",
#         "video",
#         "audio",
#         "gif",
#         "document",
#         "edited",
#     }

#     EMOJI_PATTERN = re.compile(
#         r"[\U0001f600-\U0001f64f"
#         r"\U0001f300-\U0001f5ff"
#         r"\U0001f680-\U0001f6ff"
#         r"\U0001f1e0-\U0001f1ff]"
#     )
#     WORD_PATTERN = re.compile(r"\b[a-zA-Z']+\b")

#     def compute(self, parsed_data: dict) -> dict:
#         participant_words = defaultdict(list)
#         participant_emojis = defaultdict(list)

#         group_words = []
#         group_emojis = []

#         for msg in parsed_data.get("messages", []):
#             sender = msg.get("sender", "Unknown")
#             text = msg.get("text", "").lower()

#             words = self.WORD_PATTERN.findall(text)
#             filtered_words = [
#                 w
#                 for w in words
#                 if len(w) > 2 and w not in self.STOPWORDS and w not in self.SYSTEM_WORDS
#             ]

#             emojis = self.EMOJI_PATTERN.findall(text)

#             participant_words[sender].extend(filtered_words)
#             participant_emojis[sender].extend(emojis)

#             group_words.extend(filtered_words)
#             group_emojis.extend(emojis)

#         results = {"participants": {}, "group": {}}

#         for sender in participant_words.keys():
#             word_counter = Counter(participant_words[sender])
#             emoji_counter = Counter(participant_emojis[sender])

#             vocab_size = len(set(participant_words[sender]))
#             total_words = len(participant_words[sender])
#             unique_ratio = vocab_size / total_words if total_words > 0 else 0

#             results["participants"][sender] = {
#                 "top_words": word_counter.most_common(10),
#                 "top_emojis": emoji_counter.most_common(10),
#                 "vocabulary_size": vocab_size,
#                 "unique_word_ratio": round(unique_ratio, 3),
#             }

#         group_word_counter = Counter(group_words)
#         group_emoji_counter = Counter(group_emojis)

#         results["group"] = {
#             "group_top_words": group_word_counter.most_common(15),
#             "group_top_emojis": group_emoji_counter.most_common(15),
#             "total_unique_words": len(set(group_words)),
#         }

#         return results

#     def compute_signatures(self, parsed_data: dict) -> dict:
#         base = self.compute(parsed_data)
#         signature_results = {}

#         all_group_words = []
#         for msg in parsed_data.get("messages", []):
#             text = msg.get("text", "").lower()
#             words = self.WORD_PATTERN.findall(text)
#             words = [
#                 w
#                 for w in words
#                 if len(w) > 2 and w not in self.STOPWORDS and w not in self.SYSTEM_WORDS
#             ]
#             all_group_words.extend(words)

#         group_word_counter = Counter(all_group_words)

#         for sender in base["participants"]:
#             personal_words = []

#             for msg in parsed_data.get("messages", []):
#                 if msg.get("sender") == sender:
#                     text = msg.get("text", "").lower()
#                     words = self.WORD_PATTERN.findall(text)
#                     words = [
#                         w
#                         for w in words
#                         if len(w) > 2
#                         and w not in self.STOPWORDS
#                         and w not in self.SYSTEM_WORDS
#                     ]
#                     personal_words.extend(words)

#             personal_counter = Counter(personal_words)
#             signatures = []

#             for word, count in personal_counter.items():
#                 if count > 20:
#                     group_count = group_word_counter[word]
#                     if group_count > 0:
#                         ratio = count / group_count
#                         if ratio > 0.25:
#                             signatures.append((word, round(ratio, 2)))

#             signatures.sort(key=lambda x: x[1], reverse=True)
#             signature_results[sender] = signatures[:5]

#         return signature_results
