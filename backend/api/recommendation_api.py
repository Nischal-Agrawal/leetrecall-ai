from fastapi import APIRouter

from ml.recommendation.db_recommendations import (
    generate_recommendations
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/")
def get_recommendations():

    return generate_recommendations()