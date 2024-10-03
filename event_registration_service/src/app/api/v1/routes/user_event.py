from fastapi import APIRouter, HTTPException, status


router = APIRouter()


@router.post("/events")
async def event_handler():
    """Обработчик события исходя из типа этого события."""
    return "ok"
