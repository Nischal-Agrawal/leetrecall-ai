import pandas as pd
import joblib

from backend.database.connection import SessionLocal

from backend.models.question import Question
from backend.models.solve import Solve
from backend.models.revision import Revision


model = joblib.load(
    "ml/artifacts/xgboost_model.pkl"
)


difficulty_mapping = {
    "Easy": 0,
    "Medium": 1,
    "Hard": 2
}


def generate_recommendations():

    db = SessionLocal()

    recommendations = []

    solves = db.query(Solve).all()

    for solve in solves:

        question = (
            db.query(Question)
            .filter(
                Question.id == solve.question_id
            )
            .first()
        )

        revision_count = (
            db.query(Revision)
            .filter(
                Revision.question_id
                == solve.question_id
            )
            .count()
        )

        features = pd.DataFrame(
            [
                {
                    "days_since_solved": 30,
                    "difficulty":
                    difficulty_mapping[
                        question.difficulty
                    ],
                    "wrong_attempts":
                    solve.wrong_attempts,
                    "hints_used":
                    solve.hints_used,
                    "confidence_score":
                    solve.confidence_score,
                    "revision_count":
                    revision_count
                }
            ]
        )

        remember_probability = (
            model.predict_proba(
                features
            )[0][1]
        )

        forget_probability = (
            1 - remember_probability
        )

        recommendations.append(
            {
                "question_id":
                question.id,

                "title":
                question.title,

                "forget_probability":
                round(
                    float(
                        forget_probability
                    ),
                    4
                )
            }
        )

    db.close()

    recommendations.sort(
        key=lambda x:
        x["forget_probability"],
        reverse=True
    )

    return recommendations


if __name__ == "__main__":

    results = generate_recommendations()

    print(
        "\nDATABASE RECOMMENDATIONS\n"
    )

    for r in results:

        print(
            r["title"],
            "->",
            r["forget_probability"]
        )