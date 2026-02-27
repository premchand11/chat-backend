from collections import defaultdict
from statistics import mean, stdev


class TrendEngine:

    def run(self, parsed_data: dict):

        messages = parsed_data.get("messages", [])
        if not messages:
            return self._empty_result()

        messages = sorted(messages, key=lambda x: x.get("timestamp"))

        daily_counts = defaultdict(int)
        weekly_counts = defaultdict(int)
        hourly_counts = defaultdict(int)
        participant_daily = defaultdict(lambda: defaultdict(int))

        for msg in messages:

            ts = msg.get("timestamp")
            sender = msg.get("sender")

            if not ts or not sender:
                continue

            day_key = ts.date().isoformat()
            week_key = f"{ts.year}-W{ts.isocalendar()[1]:02d}"
            hour_key = ts.hour

            daily_counts[day_key] += 1
            weekly_counts[week_key] += 1
            hourly_counts[hour_key] += 1
            participant_daily[sender][day_key] += 1

        if not daily_counts:
            return self._empty_result()

        # -------------------------
        # Peaks
        # -------------------------
        peak_day = max(daily_counts.items(), key=lambda x: x[1])
        lowest_day = min(daily_counts.items(), key=lambda x: x[1])
        peak_week = max(weekly_counts.items(), key=lambda x: x[1])
        peak_hour = max(hourly_counts.items(), key=lambda x: x[1])

        # -------------------------
        # Volatility
        # -------------------------
        daily_values = list(daily_counts.values())

        avg_daily = mean(daily_values)
        volatility = stdev(daily_values) if len(daily_values) > 1 else 0

        # -------------------------
        # Night Ratio
        # -------------------------
        night_messages = sum(
            count for hour, count in hourly_counts.items() if hour >= 22 or hour <= 4
        )

        total_messages = sum(hourly_counts.values())
        night_ratio = night_messages / total_messages if total_messages > 0 else 0

        # -------------------------
        # Surge Detection
        # -------------------------
        surge_days = []

        if volatility > 0:
            for day, count in daily_counts.items():
                if count > avg_daily + (1.5 * volatility):
                    surge_days.append({"day": day, "count": count})

        surge_days = sorted(surge_days, key=lambda x: x["count"], reverse=True)[:5]

        # -------------------------
        # Consistency
        # -------------------------
        consistency_scores = {}

        for sender, day_data in participant_daily.items():
            values = list(day_data.values())
            if len(values) > 1:
                consistency_scores[sender] = stdev(values)

        most_consistent_member = None
        if consistency_scores:
            sender, score = min(consistency_scores.items(), key=lambda x: x[1])
            most_consistent_member = {
                "name": sender,
                "consistency_score": round(score, 3),
            }

        return {
            "daily_counts": dict(daily_counts),
            "weekly_counts": dict(weekly_counts),
            "hourly_distribution": dict(hourly_counts),
            "peak_day": {"day": peak_day[0], "count": peak_day[1]},
            "lowest_day": {"day": lowest_day[0], "count": lowest_day[1]},
            "peak_week": {"week": peak_week[0], "count": peak_week[1]},
            "peak_hour": {"hour": peak_hour[0], "count": peak_hour[1]},
            "average_daily_activity": round(avg_daily, 2),
            "activity_volatility": round(volatility, 2),
            "night_activity_ratio": round(night_ratio, 3),
            "surge_days": surge_days,
            "most_consistent_member": most_consistent_member,
        }

    def _empty_result(self):
        return {
            "daily_counts": {},
            "weekly_counts": {},
            "hourly_distribution": {},
            "peak_day": None,
            "lowest_day": None,
            "peak_week": None,
            "peak_hour": None,
            "average_daily_activity": 0,
            "activity_volatility": 0,
            "night_activity_ratio": 0,
            "surge_days": [],
            "most_consistent_member": None,
        }


# from collections import defaultdict
# from statistics import mean, stdev
# from datetime import timedelta


# class TrendEngine:

#     def compute(self, parsed_data: dict):

#         messages = sorted(parsed_data["messages"], key=lambda x: x["timestamp"])

#         daily_counts = defaultdict(int)
#         weekly_counts = defaultdict(int)
#         hourly_counts = defaultdict(int)
#         participant_daily = defaultdict(lambda: defaultdict(int))

#         for msg in messages:

#             ts = msg["timestamp"]
#             sender = msg["sender"]

#             day_key = ts.date()
#             week_key = f"{ts.year}-W{ts.isocalendar()[1]}"
#             hour_key = ts.hour

#             daily_counts[day_key] += 1
#             weekly_counts[week_key] += 1
#             hourly_counts[hour_key] += 1

#             participant_daily[sender][day_key] += 1

#         # -------------------------
#         # BASIC PEAKS
#         # -------------------------
#         peak_day = max(daily_counts.items(), key=lambda x: x[1])
#         peak_week = max(weekly_counts.items(), key=lambda x: x[1])
#         peak_hour = max(hourly_counts.items(), key=lambda x: x[1])

#         # -------------------------
#         # LOWEST ACTIVITY DAY
#         # -------------------------
#         lowest_day = min(daily_counts.items(), key=lambda x: x[1])

#         # -------------------------
#         # ACTIVITY VOLATILITY
#         # -------------------------
#         daily_values = list(daily_counts.values())

#         avg_daily = mean(daily_values)
#         volatility = stdev(daily_values) if len(daily_values) > 1 else 0

#         # -------------------------
#         # NIGHT VS DAY RATIO
#         # -------------------------
#         night_messages = sum(
#             count for hour, count in hourly_counts.items() if hour >= 22 or hour <= 4
#         )
#         total_messages = sum(hourly_counts.values())

#         night_ratio = night_messages / total_messages if total_messages > 0 else 0

#         # -------------------------
#         # SURGE DETECTION
#         # -------------------------
#         surge_days = []

#         for day, count in daily_counts.items():
#             if volatility > 0 and count > avg_daily + (1.5 * volatility):
#                 surge_days.append((day, count))

#         # -------------------------
#         # TOP CONSISTENT MEMBER
#         # -------------------------
#         consistency_scores = {}

#         for sender, day_data in participant_daily.items():
#             values = list(day_data.values())
#             if len(values) > 1:
#                 consistency_scores[sender] = stdev(values)

#         most_consistent_member = None
#         if consistency_scores:
#             most_consistent_member = min(consistency_scores.items(), key=lambda x: x[1])

#         return {
#             "daily_counts": dict(daily_counts),
#             "weekly_counts": dict(weekly_counts),
#             "hourly_distribution": dict(hourly_counts),
#             "peak_day": peak_day,
#             "lowest_day": lowest_day,
#             "peak_week": peak_week,
#             "peak_hour": peak_hour,
#             "average_daily_activity": round(avg_daily, 2),
#             "activity_volatility": round(volatility, 2),
#             "night_activity_ratio": round(night_ratio, 3),
#             "surge_days": surge_days[:5],
#             "most_consistent_member": most_consistent_member,
#         }
