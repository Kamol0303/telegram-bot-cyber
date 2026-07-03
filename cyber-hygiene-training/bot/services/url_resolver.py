"""Resolve training platform base URL (tunnel or local)."""

from backend.services.url_service import get_base_url, get_tunnel_info

__all__ = ["get_base_url", "get_tunnel_info"]
