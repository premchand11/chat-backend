import asyncio
import httpx


class AIService:
    """
    Groq-powered cinematic AI summary generator.
    OpenAI-compatible endpoint.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.1-8b-instant",  # 🔥 Fast + Free tier friendly
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.semaphore = asyncio.Semaphore(3)  # limit parallel requests

    # -----------------------------------------------------
    # 🔌 Core AI Call
    # -----------------------------------------------------

    async def _call_ai(self, messages: list) -> str | None:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.9,
            "max_tokens": 400,
        }

        try:
            async with self.semaphore:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        self.base_url,
                        headers=headers,
                        json=payload,
                    )

            if response.status_code != 200:
                print("Groq API error:", response.text)
                return None

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            print("Groq exception:", str(e))
            return None

    # -----------------------------------------------------
    # 🎬 User Summaries (Parallel)
    # -----------------------------------------------------

    async def generate_user_summaries(self, users_payload: dict) -> dict:
        tasks = []

        for name, payload in users_payload.items():
            tasks.append(self._generate_single_user(name, payload))

        results = await asyncio.gather(*tasks)

        summaries = {}
        for r in results:
            if r:
                summaries.update(r)

        return summaries

    async def _generate_single_user(self, name: str, payload: dict):

        system_prompt = """
You are a witty social observer.

Write fun, playful personality summaries based on group chat behavior.
Keep it light, clever, and relatable.
No heavy drama.
No cinematic language.
No mentioning numbers or metrics.
No harsh insults.
It should feel like a smart friend describing them.
"""

        user_prompt = self._build_user_prompt(payload)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        text = await self._call_ai(messages)

        if not text:
            return {name: "The multiverse flickers... their legend remains unwritten."}

        return {name: text}

    # -----------------------------------------------------
    # 👥 Group Summary
    # -----------------------------------------------------

    async def generate_group_summary(self, group_payload: dict) -> str:

        system_prompt = """
You are a cosmic storyteller observing a powerful chat group.

Write a cinematic, dramatic group summary.
Make it feel like a movie trailer.
Never mention numbers.
Never mention metrics.
"""

        user_prompt = self._build_group_prompt(group_payload)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        text = await self._call_ai(messages)

        if not text:
            return "Across the multiverse, this group remains... undefined."

        return text

    # -----------------------------------------------------
    # 🛠 Prompt Builders
    # -----------------------------------------------------

    def _build_user_prompt(self, p: dict) -> str:
        traits = p.get("traits", {})
        behavior = p.get("behavior", {})
        return f"""
Name: {p.get("name", "Unknown")}
Archetype: {p.get("character", "Unknown")}
Role: {p.get("role", "Unknown")}
Risk: {p.get("risk_flag", "Unknown")}
Strongest Bond: {p.get("strongest_bond", "Unknown")}

Traits:
- Intensity: {traits.get("intensity")}
- Warmth: {traits.get("warmth")}
- Control: {traits.get("control")}
- Stability: {traits.get("stability")}
- Mystery: {traits.get("mystery")}
"""

    def _build_group_prompt(self, g: dict) -> str:
        return f"""
Top Influencer: {g.get("top_influencer")}
Most Ghost Prone: {g.get("most_ghost_prone")}
Group Health: {g.get("health_score")}
Night Activity: {g.get("night_activity_ratio")}
"""


# import asyncio
# import httpx


# class AIService:

#     def __init__(self, api_key: str, model: str = "openai/gpt-3.5-turbo"):
#         self.api_key = api_key
#         self.model = model
#         self.base_url = "https://openrouter.ai/api/v1/chat/completions"
#         self.semaphore = asyncio.Semaphore(3)  # 🔥 limit parallel calls

#     async def _call_ai(self, messages: list) -> str:

#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json",
#         }

#         payload = {
#             "model": self.model,
#             "messages": messages,
#             "temperature": 0.8,
#             "max_tokens": 300,
#         }

#         async with self.semaphore:  # 🔥 concurrency control
#             async with httpx.AsyncClient(timeout=30.0) as client:
#                 response = await client.post(
#                     self.base_url,
#                     headers=headers,
#                     json=payload,
#                 )

#         if response.status_code != 200:
#             return "Narrator lost signal in the multiverse. Try again."

#         data = response.json()

#         return data["choices"][0]["message"]["content"]

#     # -----------------------------------------------------
#     # 🎬 USER SUMMARIES (Parallel)
#     # -----------------------------------------------------

#     async def generate_user_summaries(self, users_payload: dict) -> dict:

#         tasks = []

#         for name, payload in users_payload.items():
#             tasks.append(self._generate_single_user(name, payload))

#         results = await asyncio.gather(*tasks, return_exceptions=True)

#         summaries = {}

#         for result in results:
#             if isinstance(result, dict):
#                 summaries.update(result)

#         return summaries

#     async def _generate_single_user(self, name: str, payload: dict):

#         system_prompt = """
# You are a dramatic social intelligence narrator.

# Write cinematic, playful, dramatic personality summaries.
# Never mention numbers.
# Never mention metrics.
# Never sound analytical.
# Make it fun and theatrical.
# Never insult.
# """

#         user_prompt = self._build_user_prompt(payload)

#         messages = [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt},
#         ]

#         try:
#             text = await self._call_ai(messages)
#             return {name: text}
#         except Exception:
#             return {name: "The cosmic narrator is temporarily offline."}

#     # -----------------------------------------------------
#     # 👥 GROUP SUMMARY
#     # -----------------------------------------------------

#     async def generate_group_summary(self, group_payload: dict) -> str:

#         system_prompt = """
# You are a dramatic group dynamic storyteller.

# Write a cinematic summary of a chat group.
# Fun. Dramatic. Theatrical.
# Never mention numbers.
# Never mention metrics.
# """

#         user_prompt = self._build_group_prompt(group_payload)

#         messages = [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt},
#         ]

#         return await self._call_ai(messages)

#     # -----------------------------------------------------
#     # 🔧 Prompt Builders
#     # -----------------------------------------------------

#     def _build_user_prompt(self, p: dict) -> str:

#         return f"""
# Generate a dramatic personality introduction.

# Name: {p["name"]}
# Universe Archetype: {p["character"]}
# Role: {p["role"]}
# Risk: {p["risk_flag"]}
# Strongest Bond: {p["strongest_bond"]}

# Personality Traits:
# - Intensity: {p["traits"]["intensity"]}
# - Warmth: {p["traits"]["warmth"]}
# - Control: {p["traits"]["control"]}
# - Stability: {p["traits"]["stability"]}
# - Mystery: {p["traits"]["mystery"]}

# Behavior:
# - Investment: {p["behavior"]["investment"]}
# - Dominance: {p["behavior"]["dominance"]}
# - Ghost Score: {p["behavior"]["ghost_score"]}
# - Dry Text Score: {p["behavior"]["dry_text_score"]}
# """

#     def _build_group_prompt(self, g: dict) -> str:

#         return f"""
# Write a cinematic group dynamic summary.

# Top Influencer: {g["top_influencer"]}
# Most Ghost Prone: {g["most_ghost_prone"]}
# Night Activity Ratio: {g["night_activity_ratio"]}
# Group Health Score: {g["health_score"]}
# """
