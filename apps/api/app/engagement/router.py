from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.engine import Engine

from ..auth import get_current_user, require_admin
from ..auth.schemas import UserOut
from ..listings.repo import ListingQueryRepo
from .repo import EngagementRepository
from .schemas import (
    AIDashboardSummary,
    EvaluationRunCreate,
    FavoriteOut,
    InteractionCreate,
    InteractionOut,
    RecommendationResponse,
    NotificationOut,
    NotificationRefreshOut,
    SavedSearchCreate,
    SavedSearchOut,
)
from .service import EngagementService
from .schemas import PreferenceQuiz

router = APIRouter(tags=["engagement"])
_service: EngagementService | None = None
_repo: EngagementRepository | None = None


def init_engagement(engine: Engine) -> None:
    global _service, _repo
    _repo = EngagementRepository(engine)
    _service = EngagementService(_repo, ListingQueryRepo(engine))


def get_service() -> EngagementService:
    if _service is None:
        raise HTTPException(503, "Engagement service chưa khởi tạo")
    return _service


def get_repo() -> EngagementRepository:
    if _repo is None:
        raise HTTPException(503, "Engagement repository chưa khởi tạo")
    return _repo


@router.post("/interactions", response_model=InteractionOut, status_code=201)
def create_interaction(
    body: InteractionCreate,
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.interaction(user.id, body)


@router.get("/favorites", response_model=list[FavoriteOut])
def favorites(
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.favorites(user.id)


@router.put("/favorites/{listing_id}", response_model=FavoriteOut)
def favorite(
    listing_id: int,
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.favorite(user.id, listing_id)


@router.delete("/favorites/{listing_id}", status_code=204)
def unfavorite(
    listing_id: int,
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    service.unfavorite(user.id, listing_id)
    return Response(status_code=204)


@router.get("/saved-searches", response_model=list[SavedSearchOut])
def saved_searches(
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.saved_searches(user.id)


@router.post("/saved-searches", response_model=SavedSearchOut, status_code=201)
def create_saved_search(
    body: SavedSearchCreate,
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.create_saved_search(user.id, body)


@router.delete("/saved-searches/{search_id}", status_code=204)
def delete_saved_search(
    search_id: int,
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    service.delete_saved_search(user.id, search_id)
    return Response(status_code=204)


@router.get("/recommend/for-you", response_model=RecommendationResponse)
@router.get("/recommendations", response_model=RecommendationResponse)
def recommendations(
    limit: int = Query(default=10, ge=1, le=30),
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.recommendations(user.id, limit)


@router.post("/recommend/quiz")
def save_quiz(
    body: PreferenceQuiz,
    user: UserOut = Depends(get_current_user),
    repo: EngagementRepository = Depends(get_repo),
):
    repo.save_preferences(user.id, body.model_dump())
    return {"ok": True, "dimensions": 384, "algorithm": "structured-cosine-v1"}


@router.get("/recommend/quiz")
def get_quiz(
    user: UserOut = Depends(get_current_user),
    repo: EngagementRepository = Depends(get_repo),
):
    return repo.preferences(user.id)


@router.post("/recommend/feedback", response_model=InteractionOut, status_code=201)
def recommend_feedback(
    body: InteractionCreate,
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.interaction(user.id, body)


@router.get("/recommend/popular", response_model=RecommendationResponse)
def popular(
    repo: EngagementRepository = Depends(get_repo),
    service: EngagementService = Depends(get_service),
):
    from .recommender import rank
    from .schemas import RecommendationItem

    _, rows = rank(repo.recommendation_candidates(), [], None, 10)
    items = [
        RecommendationItem(
            listing=listing,
            score=score / (score + 1),
            reasons=[
                "Mức quan tâm trong 30 ngày; chất lượng dùng để phân định đồng điểm"
            ],
        )
        for score, row, _ in rows
        if (listing := service.listings.get_visible(row["id"])) is not None
    ]
    return RecommendationResponse(
        cold_start=True, profile_evidence=0, items=items, algorithm="popularity-30d-v1"
    )


@router.get("/admin/ai-dashboard", response_model=AIDashboardSummary)
def ai_dashboard(
    days: int = Query(default=30, ge=1, le=365),
    _admin: UserOut = Depends(require_admin),
    service: EngagementService = Depends(get_service),
):
    return service.dashboard(days)


@router.post("/admin/evaluation-runs", status_code=201)
def create_evaluation_run(
    body: EvaluationRunCreate,
    _admin: UserOut = Depends(require_admin),
    repo: EngagementRepository = Depends(get_repo),
):
    import json

    return repo.create_evaluation_run(
        {
            **body.model_dump(exclude={"metrics"}),
            "metrics": json.dumps(body.metrics),
        }
    )


@router.get("/notifications", response_model=list[NotificationOut])
def notifications(
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.notifications(user.id)


@router.post("/notifications/refresh", response_model=NotificationRefreshOut)
def refresh_notifications(
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.refresh_notifications(user.id)


@router.patch("/notifications/{notification_id}", response_model=NotificationOut)
def mark_notification_read(
    notification_id: int,
    user: UserOut = Depends(get_current_user),
    service: EngagementService = Depends(get_service),
):
    return service.mark_notification_read(user.id, notification_id)
