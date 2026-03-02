"""
System-level views for health checks and monitoring.
Used by cron jobs and load balancers to keep the service alive.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring and cron jobs.
    Prevents Render free tier from sleeping due to inactivity.

    Returns 200 if healthy, 503 if unhealthy.
    """
    health = {
        "status": "healthy",
        "database": "unknown",
    }

    # Check database connectivity
    try:
        connection.ensure_connection()
        health["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health["status"] = "unhealthy"
        health["database"] = "disconnected"
        return Response(health, status=503)

    return Response(health, status=200)
