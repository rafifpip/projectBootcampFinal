def calculate_eco_score(stats):

    score_map = {
        "Sampah Organik": 10,
        "Sampah Anorganik": 20,
        "Sampah B3": -10
    }

    total_score = 0

    for category, count in stats.items():

        if category in score_map:
            total_score += score_map[category] * count

    return total_score


def get_eco_status(score):

    if score >= 80:
        return "Excellent 🌟"

    elif score >= 50:
        return "Good ✅"

    elif score >= 20:
        return "Fair ⚠️"

    else:
        return "Poor ❌"