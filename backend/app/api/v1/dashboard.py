from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.services.cache import get_revenue_summary
from app.services.reservations import ensure_property_belongs_to_tenant
from app.core.auth import authenticate_request as get_current_user

router = APIRouter()


@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    current_user=Depends(get_current_user),
) -> Dict[str, Any]:
    tenant_id = current_user.tenant_id

    if not tenant_id:
        raise HTTPException(
            status_code=401,
            detail="Authenticated user has no tenant",
        )

    await ensure_property_belongs_to_tenant(property_id, tenant_id)

    revenue_data = await get_revenue_summary(property_id, tenant_id)

    return {
        "property_id": revenue_data["property_id"],
        "total_revenue": revenue_data["total"],
        "currency": revenue_data["currency"],
        "reservations_count": revenue_data["count"],
    }
