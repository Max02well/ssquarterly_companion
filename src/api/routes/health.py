from fastapi import APIRouter,status

router = APIRouter()


@router.get("/health")
async def health(status_code: int = status.HTTP_200_OK):
    return {
        "status": status_code,
        "service": "quarterly-companion",
    }