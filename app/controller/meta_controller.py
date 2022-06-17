
from typing import Dict, Any

from fastapi import APIRouter


router = APIRouter(tags=["meta"], prefix="/meta")


@router.get("")
async def version() -> Dict[str, Any]:
    return {}
