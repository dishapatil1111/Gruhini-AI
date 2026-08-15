from collections import defaultdict
from statistics import mean


# ============================================================
# BASIC HELPERS
# ============================================================

def _numeric_values(values):
    """
    Return only valid numeric values.

    None and invalid values are ignored.
    """

    if not isinstance(values, list):

        return []

    return [
        float(value)
        for value in values
        if isinstance(
            value,
            (int, float)
        )
    ]


def _performance_values(history):
    """
    Return valid interview performance percentages.
    """

    if not isinstance(history, list):

        return []

    return [
        float(interview["performance"])
        for interview in history
        if isinstance(interview, dict)
        and isinstance(
            interview.get("performance"),
            (int, float)
        )
    ]


def _score_values(history):
    """
    Return all valid individual question scores.
    """

    if not isinstance(history, list):

        return []

    scores = []

    for interview in history:

        if not isinstance(
            interview,
            dict
        ):
            continue

        scores.extend(
            _numeric_values(
                interview.get(
                    "scores",
                    []
                )
            )
        )

    return scores


# ============================================================
# OVERALL STATISTICS
# ============================================================

def get_total_interviews(history):
    """
    Return the number of completed interviews.
    """

    if not isinstance(history, list):

        return 0

    return len(history)


def get_average_performance(history):
    """
    Return average interview performance percentage.

    Returns:
        float or None
    """

    values = _performance_values(
        history
    )

    if not values:

        return None

    return mean(
        values
    )


def get_best_performance(history):
    """
    Return the highest interview performance percentage.

    Returns:
        float or None
    """

    values = _performance_values(
        history
    )

    if not values:

        return None

    return max(
        values
    )


def get_lowest_performance(history):
    """
    Return the lowest interview performance percentage.

    Returns:
        float or None
    """

    values = _performance_values(
        history
    )

    if not values:

        return None

    return min(
        values
    )


def get_average_score(history):
    """
    Return the average individual question score.

    Returns:
        float or None
    """

    scores = _score_values(
        history
    )

    if not scores:

        return None

    return mean(
        scores
    )


# ============================================================
# QUESTION STATISTICS
# ============================================================

def get_total_questions(history):
    """
    Return the total number of questions
    across all completed interviews.
    """

    if not isinstance(history, list):

        return 0

    total = 0

    for interview in history:

        if not isinstance(
            interview,
            dict
        ):
            continue

        value = interview.get(
            "total_questions",
            0
        )

        if isinstance(
            value,
            (int, float)
        ):

            total += int(
                value
            )

    return total


def get_score_distribution(history):
    """
    Group individual question scores
    into performance bands.

    Returns:
        dict
    """

    scores = _score_values(
        history
    )

    distribution = {
        "Excellent (9-10)": 0,
        "Good (7-8.9)": 0,
        "Average (5-6.9)": 0,
        "Needs Improvement (<5)": 0,
    }

    for score in scores:

        if score >= 9:

            distribution[
                "Excellent (9-10)"
            ] += 1

        elif score >= 7:

            distribution[
                "Good (7-8.9)"
            ] += 1

        elif score >= 5:

            distribution[
                "Average (5-6.9)"
            ] += 1

        else:

            distribution[
                "Needs Improvement (<5)"
            ] += 1

    return distribution


# ============================================================
# INTERVIEW TYPE ANALYTICS
# ============================================================

def get_performance_by_interview_type(history):
    """
    Calculate average performance grouped
    by interview type.

    Returns:
        dict
    """

    grouped = defaultdict(list)

    if not isinstance(history, list):

        return {}

    for interview in history:

        if not isinstance(
            interview,
            dict
        ):
            continue

        interview_type = interview.get(
            "interview_type"
        )

        performance = interview.get(
            "performance"
        )

        if (
            interview_type
            and isinstance(
                performance,
                (int, float)
            )
        ):

            grouped[
                interview_type
            ].append(
                float(performance)
            )

    return {
        key: mean(values)
        for key, values in grouped.items()
    }


# ============================================================
# ROLE ANALYTICS
# ============================================================

def get_performance_by_role(history):
    """
    Calculate average performance grouped
    by job role.

    Returns:
        dict
    """

    grouped = defaultdict(list)

    if not isinstance(history, list):

        return {}

    for interview in history:

        if not isinstance(
            interview,
            dict
        ):
            continue

        role = interview.get(
            "role"
        )

        performance = interview.get(
            "performance"
        )

        if (
            role
            and isinstance(
                performance,
                (int, float)
            )
        ):

            grouped[
                role
            ].append(
                float(performance)
            )

    return {
        key: mean(values)
        for key, values in grouped.items()
    }


# ============================================================
# DIFFICULTY ANALYTICS
# ============================================================

def get_performance_by_difficulty(history):
    """
    Calculate average performance grouped
    by interview difficulty.
    """

    grouped = defaultdict(list)

    if not isinstance(history, list):

        return {}

    for interview in history:

        if not isinstance(
            interview,
            dict
        ):
            continue

        difficulty = interview.get(
            "difficulty"
        )

        performance = interview.get(
            "performance"
        )

        if (
            difficulty
            and isinstance(
                performance,
                (int, float)
            )
        ):

            grouped[
                difficulty
            ].append(
                float(performance)
            )

    return {
        key: mean(values)
        for key, values in grouped.items()
    }


# ============================================================
# PROGRESS / TREND
# ============================================================

def get_performance_trend(history):
    """
    Return interview performance in chronological order.

    Each item contains:

        interview_number
        date
        role
        performance
        average_score
    """

    if not isinstance(history, list):

        return []

    trend = []

    for index, interview in enumerate(
        history,
        start=1
    ):

        if not isinstance(
            interview,
            dict
        ):
            continue

        performance = interview.get(
            "performance"
        )

        average_score = interview.get(
            "average_score"
        )

        if not isinstance(
            performance,
            (int, float)
        ):

            continue

        trend.append(
            {
                "interview_number": index,
                "date": interview.get(
                    "date"
                ),
                "role": interview.get(
                    "role"
                ),
                "performance": float(
                    performance
                ),
                "average_score": (
                    float(average_score)
                    if isinstance(
                        average_score,
                        (int, float)
                    )
                    else None
                ),
            }
        )

    return trend


def get_improvement(history):
    """
    Calculate improvement between the first
    and latest valid interview.

    Returns:
        float or None

    Positive = improvement.
    Negative = decline.
    Zero = no change.
    """

    trend = get_performance_trend(
        history
    )

    if len(trend) < 2:

        return None

    first = trend[0][
        "performance"
    ]

    latest = trend[-1][
        "performance"
    ]

    return latest - first


def get_latest_performance(history):
    """
    Return the performance of the latest
    valid interview.

    Returns:
        float or None
    """

    trend = get_performance_trend(
        history
    )

    if not trend:

        return None

    return trend[-1][
        "performance"
    ]


# ============================================================
# COMPLETE ANALYTICS SUMMARY
# ============================================================

def get_interview_analytics(history):
    """
    Return a complete analytics summary.

    This function is intended to provide
    one convenient interface for the UI.
    """

    return {
        "total_interviews": get_total_interviews(
            history
        ),

        "average_performance": get_average_performance(
            history
        ),

        "best_performance": get_best_performance(
            history
        ),

        "lowest_performance": get_lowest_performance(
            history
        ),

        "average_score": get_average_score(
            history
        ),

        "total_questions": get_total_questions(
            history
        ),

        "score_distribution": get_score_distribution(
            history
        ),

        "performance_by_interview_type": (
            get_performance_by_interview_type(
                history
            )
        ),

        "performance_by_role": (
            get_performance_by_role(
                history
            )
        ),

        "performance_by_difficulty": (
            get_performance_by_difficulty(
                history
            )
        ),

        "performance_trend": (
            get_performance_trend(
                history
            )
        ),

        "improvement": get_improvement(
            history
        ),

        "latest_performance": (
            get_latest_performance(
                history
            )
        ),
    }