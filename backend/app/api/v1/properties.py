from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.core.auth import authenticate_request as get_current_user
from app.core.database_pool import db_pool

router = APIRouter()


@router.get("/properties")
async def get_properties(
    current_user=Depends(get_current_user),
) -> List[Dict[str, Any]]:
    tenant_id = current_user.tenant_id
    if not tenant_id:
        return []

    if db_pool.session_factory is None:
        await db_pool.initialize()

    if db_pool.session_factory is None:
        raise RuntimeError("Database pool is not initialized")

    async with db_pool.get_session() as session:
        result = await session.execute(
            text("""
                SELECT id, name, timezone
                FROM properties
                WHERE tenant_id = :tenant_id
                ORDER BY name
            """),
            {"tenant_id": tenant_id},
        )

        return [
            {
                "id": row.id,
                "name": row.name,
                "timezone": row.timezone,
            }
            for row in result.fetchall()
        ]
