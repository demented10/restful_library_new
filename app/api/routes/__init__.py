from .publishers import router as publishers_router
from .books import router as books_router
from .readers import router as readers_router
from .borrowings import router as borrowings_router
from .reports import router as reports_router

__all__ = [
    "publishers_router",
    "books_router", 
    "readers_router",
    "borrowings_router",
    "reports_router",
]