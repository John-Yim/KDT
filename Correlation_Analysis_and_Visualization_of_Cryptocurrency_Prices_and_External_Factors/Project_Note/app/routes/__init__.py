# app/routes/__init__.py

from .main import main_bp
from .brain import brain_bp
from .complaint import complaint_bp
from .analysis import analysis_bp

__all__ = ["main_bp", "brain_bp", "complaint_bp", "analysis_bp"]