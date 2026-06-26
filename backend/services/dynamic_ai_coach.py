from ml.recommendation.db_recommendations import (
    generate_recommendations
)

from backend.services.openai_coach import (
    generate_ai_advice
)


def get_dynamic_advice():

    recommendations = (
        generate_recommendations()
    )

    results = []

    top_questions = recommendations[:5]

    for question in top_questions:

        advice = generate_ai_advice(
            question=question["title"],
            forget_probability=
            question["forget_probability"]
        )

        results.append(
            {
                "question":
                question["title"],

                "forget_probability":
                question["forget_probability"],

                "advice":
                advice
            }
        )

    return results