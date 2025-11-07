from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol, List, Mapping, Any
from importlib import import_module
from django.conf import settings


@dataclass(slots=True)
class ProjectDTO:
    name: str
    year: str | None = None
    description: str | None = None


@dataclass(slots=True)
class CVPdfData:
    id: int
    firstname: str
    lastname: str
    bio: str | None = None
    skills: List[str] = field(default_factory=list)
    projects: List[ProjectDTO] = field(default_factory=list)
    contacts: Mapping[str, Any] = field(default_factory=dict)

    @property
    def full_name(self) -> str:
        return f"{self.firstname} {self.lastname}".strip()


class PdfRenderer(Protocol):
    def render(self, data: CVPdfData) -> bytes: ...


def _import_from_path(path: str):
    module_path, _, class_name = path.rpartition(".")
    if not module_path:
        raise ImportError(f"Invalid dotted path: {path}")
    module = import_module(module_path)
    return getattr(module, class_name)


def get_renderer() -> PdfRenderer:

    dotted = getattr(
        settings,
        "CV_PDF_RENDERER",
        "cv_app.services.pdf.reportlab_renderer.ReportLabRenderer",
    )
    cls = _import_from_path(dotted)
    return cls()  # type: ignore[return-value]
